from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.novel_page import NovelPage
from app.models.novel_promo import NovelPromo
from app.models.platform import Platform
from app.schemas.common import fail, ok
from app.services.novel_service import current_reads

router = APIRouter()


@router.get("/platforms")
def platforms_api(db: Session = Depends(get_db)):
    """投放平台列表（A端选择平台用）"""
    ps = db.query(Platform).order_by(Platform.sort.asc(), Platform.id.asc()).all()
    return ok([{"code": p.code, "name": p.name} for p in ps])


@router.get("/novel/{code}/reads")
def reads_api(code: str, db: Session = Depends(get_db)):
    p = db.query(NovelPage).filter(NovelPage.page_code == code).first()
    if not p:
        return fail("page not found", code=40404)
    p.refresh_count = (p.refresh_count or 0) + 1
    db.commit()
    db.refresh(p)
    return ok({"reads": current_reads(p), "refresh_count": p.refresh_count})


@router.get("/novel_promo/{code}")
def novel_promo_visit(code: str, db: Session = Depends(get_db)):
    """网文推广落地页访问：每打开一次访问量 +1，返回展示阅读量（基础值 + 访问次数）"""
    p = db.query(NovelPromo).filter(NovelPromo.code == code).first()
    if not p:
        return fail("page not found", code=40404)
    p.visits = (p.visits or 0) + 1
    db.commit()
    db.refresh(p)
    base = int(p.base_reads or 0)
    visits = int(p.visits or 0)
    return ok({"code": p.code, "promo_content": p.promo_content,
               "base_reads": base, "visits": visits, "reads": base + visits,
               "date": p.created_at.strftime("%Y-%m-%d") if p.created_at else ""})
