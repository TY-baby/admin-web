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
from app.utils.excel_export import export_rows_to_xlsx, export_rows_to_xlsx_merged
from app.utils.id_generator import (EXPOSURE_TIER_PRICE, EXPOSURE_TIER_RANGE, LAUNCH_TYPE_LABEL,
                                    NOVEL_PROMO_TIER_PRICE, NOVEL_PROMO_READ_RANGE,
                                    NOVEL_PROMO_URL_PREFIX,
                                    TIER_DAILY_BUDGET, TIER_ITEM_RANGE,
                                    gen_launch_items, gen_novel_promo_items, load_item_batches)
from app.utils.timeutil import now_cn

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
             keyword_phone: Optional[str] = None, launch_type: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             launch_from: Optional[date] = None, launch_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    lf = datetime.combine(launch_from, time.min) if launch_from else None
    lt = datetime.combine(launch_to, time.max) if launch_to else None
    items, total = list_customers(db, keyword_name, keyword_douyin, df, dt, page, page_size,
                                  launch_type=launch_type, phone=keyword_phone,
                                  launch_from=lf, launch_to=lt)
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
               launch_from: Optional[date] = None, launch_to: Optional[date] = None,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    if not launch_type:
        return fail("导出前必须先选择类型（首充/直播曝光度/网文推广）", code=40004)
    if launch_type not in ("FIRST_CHARGE", "EXPOSURE", "NOVEL_PROMO"):
        return fail("类型参数非法", code=40004)
    if not keyword_name and not keyword_douyin and not keyword_phone \
            and not date_from and not date_to and not launch_from and not launch_to:
        return fail("必须先输入查询条件进行导出", code=40003)
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    lf = datetime.combine(launch_from, time.min) if launch_from else None
    lt = datetime.combine(launch_to, time.max) if launch_to else None
    items, _ = list_customers(db, keyword_name, keyword_douyin, df, dt, 1, 10000,
                              launch_type=launch_type, phone=keyword_phone,
                              launch_from=lf, launch_to=lt)
    pname = {p.code: p.name for p in db.query(Platform).all()}
    is_exposure = launch_type == "EXPOSURE"
    is_novel = launch_type == "NOVEL_PROMO"
    type_label = LAUNCH_TYPE_LABEL.get(launch_type, "")
    value_col = "热度" if is_exposure else "总充值金额"
    if is_novel:
        headers = ["客户UID", "客户名称", "联系人", "手机号", "投放ID", "名称",
                   "投放平台名称", "消耗金额", "类型", "档位", "网址", "阅读量", "投放日期"]
    else:
        headers = ["客户UID", "客户名称", "联系人", "手机号", "投放ID", "名称",
                   "投放平台名称", "消耗金额", "档位"]
        if not is_exposure:
            headers += ["ID", "昵称"]
        headers += [value_col, "类型", "投放日期"]
    rows = []
    for c in items:
        dl = getattr(c, "douyin_list", []) or []
        if not dl:
            continue
        for a in dl:
            launch_date = a.launch_at.strftime("%Y-%m-%d") if a.launch_at else ""
            base = [c.customer_uid, c.customer_name, c.contact_name, c.phone,
                    a.douyin_id, a.douyin_name,
                    pname.get(a.platform_code, a.platform_code)]
            if not (a.tier and a.launch_at):
                continue
            batches = load_item_batches(a.generated_items)
            if not batches:
                price = (EXPOSURE_TIER_PRICE if is_exposure
                         else NOVEL_PROMO_TIER_PRICE if is_novel
                         else TIER_DAILY_BUDGET)[a.tier]
                budget = float(a.daily_budget or 0)
                cnt = max(1, int(budget // price)) if budget else 1
                if is_novel:
                    fake_items = gen_novel_promo_items(cnt, NOVEL_PROMO_READ_RANGE[a.tier], "")
                else:
                    rng = EXPOSURE_TIER_RANGE[a.tier] if is_exposure else TIER_ITEM_RANGE[a.tier]
                    fake_items = gen_launch_items(cnt, rng, platform_code=a.platform_code)
                batches = [{"launch_at": None, "tier": a.tier,
                            "launch_type": a.launch_type,
                            "consumed": round(cnt * price, 2),
                            "items": fake_items}]
            for b in batches:
                b_tier = b.get("tier") or a.tier
                b_type = b.get("launch_type") or a.launch_type
                if b_type != launch_type:
                    continue
                b_type_label = LAUNCH_TYPE_LABEL.get(b_type, "")
                price_map = (EXPOSURE_TIER_PRICE if b_type == "EXPOSURE"
                             else NOVEL_PROMO_TIER_PRICE if b_type == "NOVEL_PROMO"
                             else TIER_DAILY_BUDGET)
                b_consumed = float(price_map.get(b_tier, 0) or 0)
                ld = (b.get("launch_at") or "")[:10] or launch_date
                for it in b["items"]:
                    if is_novel:
                        url = NOVEL_PROMO_URL_PREFIX + str(it.get("url_code", ""))
                        pc = it.get("platform_code") or a.platform_code
                        row = base[:]
                        row[4] = ""
                        row[5] = ""
                        row[6] = pname.get(pc, pc)
                        rows.append(row + [b_consumed, b_type_label, b_tier,
                                            url, it.get("value", ""), ld])
                        continue
                    id_cols = [] if is_exposure else [it.get("biz_code", ""), it.get("nickname", "")]
                    rows.append(base + [b_consumed, b_tier] + id_cols +
                                [it.get("value", ""), b_type_label, ld])
    content = export_rows_to_xlsx(headers, rows)
    fname = f"customers_{type_label}_{now_cn().strftime('%Y%m%d%H%M%S')}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})
