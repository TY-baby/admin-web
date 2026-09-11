from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ClickLog
from ..schemas import ClickRequest
from ..security import get_client_ip

router = APIRouter()


@router.post("")
def record_click(payload: ClickRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    log = ClickLog(
        news_id=payload.news_id or 0,
        title=payload.title or "",
        fee=payload.fee or 0,
        url=payload.url or "",
        ip=ip,
    )
    db.add(log)
    db.commit()
    print(f"[CLICK] title={log.title} fee={log.fee} ip={ip}")
    return {"code": 0, "message": "点击已记录", "data": {"ip": ip, "id": log.id}}