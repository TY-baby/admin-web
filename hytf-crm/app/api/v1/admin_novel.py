from datetime import date, datetime, time
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.models.novel_page import NovelPage
from app.schemas.common import ok
from app.services.customer_service import list_customers, to_customer_item
from app.services.novel_service import current_reads, page_link

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None, keyword_douyin: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    cid_set = {cid for (cid,) in db.query(NovelPage.customer_id).distinct().all()}
    if not cid_set:
        return ok({"total": 0, "page": page, "page_size": page_size, "items": []})
    items, total = list_customers(db, keyword_name, keyword_douyin, df, dt, page, page_size,
                                  only_ids=cid_set)
    acc_ids = [a.id for c in items for a in (getattr(c, "douyin_list", []) or [])]
    pages_map = {}
    if acc_ids:
        ps = (db.query(NovelPage).filter(NovelPage.account_id.in_(acc_ids))
              .order_by(NovelPage.created_at.desc()).all())
        for p in ps:
            pages_map.setdefault(p.account_id, []).append({
                "id": p.id, "page_code": p.page_code, "link": page_link(p),
                "tier": p.tier, "unit_price": p.unit_price, "consumed": float(p.consumed),
                "reads": current_reads(p), "refresh_count": p.refresh_count,
                "created_at": p.created_at,
            })
    out = []
    for c in items:
        d = to_customer_item(c)
        for a in d["douyin_list"]:
            a["novel_pages"] = pages_map.get(a["id"], [])
        out.append(d)
    return ok({"total": total, "page": page, "page_size": page_size, "items": out})