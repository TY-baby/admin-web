from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.novel_page import NovelPage
from app.schemas.common import fail, ok
from app.services.novel_service import current_reads

router = APIRouter()


@router.get("/novel/{code}/reads")
def reads_api(code: str, db: Session = Depends(get_db)):
    p = db.query(NovelPage).filter(NovelPage.page_code == code).first()
    if not p:
        return fail("page not found", code=40404)
    p.refresh_count = (p.refresh_count or 0) + 1
    db.commit()
    db.refresh(p)
    return ok({"reads": current_reads(p), "refresh_count": p.refresh_count})