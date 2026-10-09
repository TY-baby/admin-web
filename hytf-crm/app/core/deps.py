from typing import Optional
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.admin_user import AdminUser


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _extract(authorization: Optional[str]) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="未登录或Token缺失")
    return authorization.split(" ", 1)[1].strip()


def get_current_client(authorization: Optional[str] = Header(default=None)) -> dict:
    payload = decode_token(_extract(authorization))
    if not payload or payload.get("role") != "client":
        raise HTTPException(status_code=401, detail="Token无效")
    return payload


def get_current_admin(authorization: Optional[str] = Header(default=None)) -> dict:
    payload = decode_token(_extract(authorization))
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=401, detail="管理员Token无效")
    return payload


def get_current_super(authorization: Optional[str] = Header(default=None),
                      db: Session = Depends(get_db)) -> dict:
    """仅 yy（role=super）可访问：日志、监控、账号管理"""
    payload = get_current_admin(authorization)
    u = db.query(AdminUser).filter(AdminUser.id == int(payload["sub"])).first()
    if not u or u.role != "super":
        raise HTTPException(status_code=403, detail="无权限访问")
    return payload
