from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.logging_conf import logger
from app.middlewares.rate_limit import limiter
from app.schemas.auth import ClientLoginReq
from app.schemas.common import fail, ok
from app.services.auth_service import client_login

router = APIRouter()


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, body: ClientLoginReq, db: Session = Depends(get_db)):
    data = client_login(db, body.phone, body.password)
    if not data:
        logger.warning(f"[A-login fail] phone={body.phone}")
        return fail("手机号或密码错误", code=40001)
    return ok(data)