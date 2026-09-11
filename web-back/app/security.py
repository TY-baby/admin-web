import os
import base64
import hashlib
import datetime
import jwt
from fastapi import Header, HTTPException, Request
from .config import settings


def hash_password(pwd: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, 100000)
    return base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()


def verify_password(pwd: str, hashed: str) -> bool:
    try:
        salt_b64, dk_b64 = hashed.split("$")
        salt = base64.b64decode(salt_b64)
        dk = base64.b64decode(dk_b64)
        dk2 = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, 100000)
        return dk == dk2
    except Exception:
        return False


def create_token(data: dict) -> str:
    payload = {
        **data,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_EXPIRES_MIN),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少 token")
    token = authorization.replace("Bearer ", "")
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="token 无效或已过期")


def get_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    return request.client.host if request.client else "unknown"