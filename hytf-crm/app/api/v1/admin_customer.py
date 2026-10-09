from datetime import datetime, date, time
from io import BytesIO
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.models.platform import Platform
from app.schemas.common import fail, ok
from app.schemas.customer import CustomerCreateReq, CustomerUpdateReq, DouyinUpdateReq
from app.services.customer_service import (create_customer, delete_customer, delete_douyin,
                                            list_customers,
                                            to_customer_item, update_customer, update_douyin)
from app.utils.excel_export import export_rows_to_xlsx_merged
from app.utils.id_generator import (EXPOSURE_TIER_PRICE, EXPOSURE_TIER_RANGE, LAUNCH_TYPE_LABEL,
                                    TIER_DAILY_BUDGET, TIER_ITEM_RANGE,
                                    gen_launch_items, load_items)

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
             keyword_phone: Optional[str] = None, launch_type: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, total = list_customers(db, keyword_name, keyword_douyin, df, dt, page, page_size,
                                  launch_type=launch_type, phone=keyword_phone)
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [to_customer_item(c) for c in items]})


@router.post("/create")
def create_api(body: CustomerCreateReq, db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    try:
        c = create_customer(db, body)
        return ok({"id": c.id, "customer_uid": c.customer_uid})
    except ValueError as e:
        return fail(str(e), code=40002)


@router.put("/{cid}")
def update_api(cid: int, body: CustomerUpdateReq,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    try:
        return ok({"id": update_customer(db, cid, body).id})
    except ValueError as e:
        return fail(str(e), code=40002)


@router.put("/douyin/{aid}")
def update_dy(aid: int, body: DouyinUpdateReq,
              db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    try:
        return ok({"id": update_douyin(db, aid, body).id})
    except ValueError as e:
        return fail(str(e), code=40002)


@router.delete("/{cid}")
def delete_api(cid: int, db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    delete_customer(db, cid)
    return ok()


@router.delete("/douyin/{aid}")
def delete_dy_api(aid: int, db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    delete_douyin(db, aid)
    return ok()


@router.get("/export")
def export_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
               keyword_phone: Optional[str] = None, launch_type: Optional[str] = None,
               date_from: Optional[date] = None, date_to: Optional[date] = None,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    # 需求 3.2：导出必须选类型
    if not launch_type:
        return fail("导出前必须先选择类型（首充/直播曝光度）", code=40004)
    if launch_type not in ("FIRST_CHARGE", "EXPOSURE"):
        return fail("类型参数非法", code=40004)
    if not keyword_name and not keyword_douyin and not keyword_phone \
            and not date_from and not date_to:
        return fail("必须先输入查询条件进行导出", code=40003)
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, _ = list_customers(db, keyword_name, keyword_douyin, df, dt, 1, 10000,
                              launch_type=launch_type, phone=keyword_phone)
    pname = {p.code: p.name for p in db.query(Platform).all()}
    is_exposure = launch_type == "EXPOSURE"
    # 需求 3.3：日预算→总充值金额、授权开始→投放日期、业务码→ID
    # 需求 3.4：首充展示"总充值金额"，曝光度展示"1h曝光度"
    value_col = "1h曝光度" if is_exposure else "总充值金额"
    headers = ["客户UID", "客户名称", "联系人", "手机号", "投放ID", "名称",
               "投放平台名称", "充值金额", "档位", "ID", "昵称",
               value_col, "类型", "投放日期"]
    type_label = LAUNCH_TYPE_LABEL.get(launch_type, "")
    rows = []
    merge_groups = []
    for c in items:
        group_start = len(rows)
        dl = getattr(c, "douyin_list", []) or []
        if not dl:
            rows.append([c.customer_uid, c.customer_name, c.contact_name, c.phone,
                         "", "", "", "", "", "", "", "", "", ""])
        for a in dl:
            launch_date = a.launch_at.strftime("%Y-%m-%d") if a.launch_at else ""
            base = [c.customer_uid, c.customer_name, c.contact_name, c.phone,
                    a.douyin_id, a.douyin_name,
                    pname.get(a.platform_code, a.platform_code),
                    float(a.recharge_amount)]
            if not (a.tier and a.launch_at):
                rows.append(base + ["-", "-", "-", "-", "", ""])
                continue
            # 关键：优先使用投放时落库的 generated_items，历史数据回退实时生成（不落库）
            stored = load_items(a.generated_items)
            if not stored:
                price = (EXPOSURE_TIER_PRICE if is_exposure else TIER_DAILY_BUDGET)[a.tier]
                rng = EXPOSURE_TIER_RANGE[a.tier] if is_exposure else TIER_ITEM_RANGE[a.tier]
                budget = float(a.daily_budget or 0)
                cnt = max(1, int(budget // price)) if budget else 1
                stored = gen_launch_items(cnt, rng)
            for it in stored:
                rows.append(base + [a.tier, it.get("biz_code", ""), it.get("nickname", ""),
                                    it.get("value", ""), type_label, launch_date])
        if len(rows) - 1 >= group_start:
            merge_groups.append((group_start, len(rows) - 1))
    content = export_rows_to_xlsx_merged(headers, rows, merge_groups, (0, 1, 2, 3))
    fname = f"customers_{type_label}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})
