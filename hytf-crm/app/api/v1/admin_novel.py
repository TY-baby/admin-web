from datetime import date, datetime, time
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.models.douyin_account import DouyinAccount
from app.models.novel_promo import NovelPromo
from app.schemas.common import ok, fail
from app.schemas.customer import NovelCustomerCreateReq
from app.services.customer_service import (create_novel_customer, list_customers,
                                            to_customer_item)

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             launch_from: Optional[date] = None, launch_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    """网文客户列表：仅含网文专用账号(is_promo_only)的客户，与用户管理完全隔离"""
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    lf = datetime.combine(launch_from, time.min) if launch_from else None
    lt = datetime.combine(launch_to, time.max) if launch_to else None
    cid_set = {cid for (cid,) in db.query(DouyinAccount.customer_id)
               .filter(DouyinAccount.is_promo_only == 1).distinct().all()}
    if not cid_set:
        return ok({"total": 0, "page": page, "page_size": page_size, "items": []})
    items, total = list_customers(db, keyword_name, None, df, dt, page, page_size,
                                  only_ids=cid_set, launch_from=lf, launch_to=lt)
    cids = [c.id for c in items]
    url_count = {}
    if cids:
        for cid, cnt in (db.query(NovelPromo.customer_id, func.count(NovelPromo.id))
                         .filter(NovelPromo.customer_id.in_(cids))
                         .group_by(NovelPromo.customer_id).all()):
            url_count[cid] = int(cnt or 0)
    out = []
    for c in items:
        d = to_customer_item(c)
        accs = d.get("douyin_list") or []
        promo_acc = next((a for a in accs if a.get("is_promo_only") == 1), None)
        launch_times = [a.get("launch_at") for a in accs if a.get("launch_at")]
        d["url_count"] = url_count.get(c.id, 0)
        d["total_recharge"] = round(sum(float(a.get("recharge_amount") or 0) for a in accs), 2)
        d["total_balance"] = round(sum(float(a.get("balance") or 0) for a in accs), 2)
        d["launch_at"] = max(launch_times) if launch_times else None
        d["promo_account_id"] = promo_acc.get("id") if promo_acc else (accs[0].get("id") if accs else None)
        out.append(d)
    return ok({"total": total, "page": page, "page_size": page_size, "items": out})


@router.post("/customer/create")
def create_novel_customer_api(body: NovelCustomerCreateReq,
                              db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    try:
        c = create_novel_customer(db, body)
        return ok({"id": c.id, "customer_uid": c.customer_uid})
    except ValueError as e:
        return fail(str(e), code=40002)
