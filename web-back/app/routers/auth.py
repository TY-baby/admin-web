from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import LoginRequest
from ..security import verify_password, create_token, get_current_user

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token({"userId": user.id, "username": user.username})
    return {"code": 0, "message": "登录成功", "data": {"token": token, "userInfo": user.to_dict()}}


@router.get("/info")
def info(current=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current.get("userId")).first()
    return {"code": 0, "message": "ok", "data": user.to_dict() if user else None}