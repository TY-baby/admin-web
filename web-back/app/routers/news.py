from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import News

router = APIRouter()


@router.get("")
def list_news(db: Session = Depends(get_db)):
    items = db.query(News).order_by(News.publish_time.desc()).all()
    return {"code": 0, "message": "ok", "data": {"list": [n.to_dict() for n in items]}}


@router.get("/{news_id}")
def get_news(news_id: int, db: Session = Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {"code": 0, "message": "ok", "data": item.to_dict()}