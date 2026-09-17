from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.common import ok
from app.services.dashboard_service import admin_dashboard

router = APIRouter()


@router.get("/overview")
def overview(days: int = Query(14, ge=1, le=90),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    return ok(admin_dashboard(db, days))