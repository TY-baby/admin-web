from typing import Optional
from fastapi import Header, HTTPException
from app.core.security import decode_token
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _extract(authorization: Optional[str]) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="鏈櫥褰曟垨Token缂哄け")
    return authorization.split(" ", 1)[1].strip()


def get_current_client(authorization: Optional[str] = Header(default=None)) -> dict:
    payload = decode_token(_extract(authorization))
    if not payload or payload.get("role") != "client":
        raise HTTPException(status_code=401, detail="Token鏃犳晥")
    return payload


def get_current_admin(authorization: Optional[str] = Header(default=None)) -> dict:
    payload = decode_token(_extract(authorization))
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=401, detail="绠＄悊鍛楾oken鏃犳晥")
    return payload