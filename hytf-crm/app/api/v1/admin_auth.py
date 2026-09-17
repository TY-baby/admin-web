from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.logging_conf import logger
from app.middlewares.rate_limit import limiter
from app.schemas.auth import AdminLoginReq
from app.schemas.common import fail, ok
from app.services.auth_service import admin_login

router = APIRouter()


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, body: AdminLoginReq, db: Session = Depends(get_db)):
    data = admin_login(db, body.username, body.password)
    if not data:
        logger.warning(f"[B-login fail] username={body.username}")
        return fail("账号或密码错误", code=40001)
    return ok(data)
