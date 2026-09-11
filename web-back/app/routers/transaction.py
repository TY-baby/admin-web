from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ClickLog
from ..security import get_current_user

router = APIRouter()


@router.get("")
def list_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: str = Query("", description="按新闻标题模糊搜索"),
    current=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = db.query(ClickLog).order_by(ClickLog.click_time.asc()).all()

    groups = {}
    for log in logs:
        key = log.news_id if log.news_id else "title::" + str(log.title)
        g = groups.get(key)
        if not g:
            g = {
                "news_id": log.news_id,
                "title": log.title,
                "fee": float(log.fee or 0),
                "click_count": 0,
                "click_time": None,
                "ip": log.ip,
            }
            groups[key] = g
        g["click_count"] += 1
        g["fee"] = float(log.fee or 0)
        if g["click_time"] is None or (log.click_time and log.click_time > g["click_time"]):
            g["click_time"] = log.click_time
            g["ip"] = log.ip

    result = list(groups.values())
    if keyword:
        result = [r for r in result if keyword in (r["title"] or "")]
    result.sort(key=lambda x: x["click_count"], reverse=True)

    total = len(result)
    total_click = sum(r["click_count"] for r in result)
    total_fee = round(sum(r["fee"] for r in result), 2)

    start = (page - 1) * size
    page_items = result[start:start + size]
    for r in page_items:
        r["click_time"] = r["click_time"].strftime("%Y-%m-%d %H:%M:%S") if r["click_time"] else ""

    return {
        "code": 0,
        "message": "ok",
        "data": {
            "list": page_items,
            "total": total,
            "summary": {"total_click": total_click, "total_fee": total_fee},
        },
    }