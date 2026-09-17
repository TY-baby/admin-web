from datetime import datetime, date, time
from io import BytesIO
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.common import fail, ok
from app.schemas.customer import CustomerCreateReq, CustomerUpdateReq, DouyinUpdateReq
from app.services.customer_service import (create_customer, delete_customer, list_customers,
                                            to_customer_item, update_customer, update_douyin)
from app.utils.excel_export import export_rows_to_xlsx

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, total = list_customers(db, keyword_name, keyword_douyin, df, dt, page, page_size)
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


@router.get("/export")
def export_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
               date_from: Optional[date] = None, date_to: Optional[date] = None,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, _ = list_customers(db, keyword_name, keyword_douyin, df, dt, 1, 10000)
    headers = ["客户UID", "客户名称", "联系人", "手机号", "抖音号ID", "抖音号名称",
               "6位业务码", "昵称", "充值金额", "剩余流水", "档位", "日预算",
               "授权类型", "授权开始", "授权到期", "状态", "备注", "添加时间"]
    rows = []
    for c in items:
        dl = getattr(c, "douyin_list", []) or []
        if not dl:
            rows.append([c.customer_uid, c.customer_name, c.contact_name, c.phone,
                         "", "", "", "", 0, 0, "", 0, "", "", "", "", c.remark,
                         c.created_at.strftime("%Y-%m-%d %H:%M:%S")])
            continue
        for a in dl:
            rows.append([c.customer_uid, c.customer_name, c.contact_name, c.phone,
                         a.douyin_id, a.douyin_name, a.auto_code, a.nickname,
                         float(a.recharge_amount), float(a.balance), a.tier, a.tier_daily_budget,
                         a.auth_duration,
                         a.auth_start_at.strftime("%Y-%m-%d") if a.auth_start_at else "",
                         a.auth_end_at.strftime("%Y-%m-%d") if a.auth_end_at else "不限",
                         a.status, a.remark, a.created_at.strftime("%Y-%m-%d %H:%M:%S")])
    content = export_rows_to_xlsx(headers, rows)
    fname = f"customers_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})
