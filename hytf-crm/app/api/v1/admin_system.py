from collections import deque
from datetime import datetime, date, time
from typing import Optional
import psutil
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.deps import get_current_super, get_db
from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.operation_log import OperationLog
from app.schemas.common import ok, fail
from app.services.auth_service import ALL_MENUS

router = APIRouter()


# ---------- 5.2 操作日志 ----------
@router.get("/log/list")
def log_list(keyword_username: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_super)):
    q = db.query(OperationLog)
    if keyword_username:
        q = q.filter(OperationLog.username.like(f"%{keyword_username}%"))
    if date_from:
        q = q.filter(OperationLog.created_at >= datetime.combine(date_from, time.min))
    if date_to:
        q = q.filter(OperationLog.created_at <= datetime.combine(date_to, time.max))
    total = q.count()
    items = q.order_by(OperationLog.created_at.desc()) \
        .offset((page - 1) * page_size).limit(page_size).all()
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{"id": l.id, "username": l.username, "role": l.role,
                          "action": l.action, "method": l.method, "path": l.path,
                          "ip": l.ip, "created_at": l.created_at} for l in items]})


# ---------- 5.3 服务器监控 ----------
@router.get("/monitor/stats")
def monitor_stats(_a=Depends(get_current_super)):
    vm = psutil.virtual_memory()
    du = psutil.disk_usage("/")
    cpu = psutil.cpu_percent(interval=0.3)
    return ok({
        "cpu": cpu, "cpu_count": psutil.cpu_count(),
        "mem": vm.percent, "mem_total": vm.total, "mem_used": vm.used,
        "disk": du.percent, "disk_total": du.total, "disk_used": du.used,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()),
        "cpu_threshold": settings.ALERT_CPU_THRESHOLD,
        "mem_threshold": settings.ALERT_MEM_THRESHOLD,
        "alerts": {
            "cpu": cpu > settings.ALERT_CPU_THRESHOLD,
            "mem": vm.percent > settings.ALERT_MEM_THRESHOLD,
            "disk": du.percent > 90,
        }
    })


# ---------- 5.5/5.6 普通用户（B端账号）管理 ----------
@router.get("/account/list")
def account_list(db: Session = Depends(get_db), _a=Depends(get_current_super)):
    users = db.query(AdminUser).order_by(AdminUser.id.asc()).all()
    return ok([{"id": u.id, "username": u.username, "real_name": u.real_name,
                "role": u.role, "menus": u.menus, "is_active": u.is_active,
                "last_login_at": u.last_login_at, "created_at": u.created_at} for u in users])


@router.get("/account/menus")
def account_menus(_a=Depends(get_current_super)):
    return ok(ALL_MENUS)


@router.post("/account/create")
def account_create(payload: dict, db: Session = Depends(get_db), _a=Depends(get_current_super)):
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    if not username or len(password) < 6:
        return fail("账号不能为空且密码至少6位", code=40002)
    if db.query(AdminUser).filter(AdminUser.username == username).first():
        return fail("账号已存在", code=40002)
    menus = ",".join(payload.get("menus") or [])
    u = AdminUser(username=username, password_hash=hash_password(password),
                  real_name=payload.get("real_name") or "",
                  role=payload.get("role") or "user", menus=menus, is_active=True)
    db.add(u)
    db.commit()
    db.refresh(u)
    return ok({"id": u.id})


@router.put("/account/{uid}")
def account_update(uid: int, payload: dict, db: Session = Depends(get_db), _a=Depends(get_current_super)):
    u = db.query(AdminUser).filter(AdminUser.id == uid).first()
    if not u:
        return fail("账号不存在", code=40404)
    if payload.get("real_name") is not None:
        u.real_name = payload["real_name"]
    if payload.get("menus") is not None:
        u.menus = ",".join(payload["menus"])
    if payload.get("is_active") is not None:
        u.is_active = bool(payload["is_active"])
    if payload.get("password"):
        if len(payload["password"]) < 6:
            return fail("密码至少6位", code=40002)
        u.password_hash = hash_password(payload["password"])
    db.commit()
    return ok({"id": u.id})