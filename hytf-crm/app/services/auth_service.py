from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import build_client_default_password, create_access_token, verify_password
from app.models.admin_user import AdminUser
from app.models.customer import Customer

ALL_MENUS = ["dashboard", "customer", "novel", "invoice", "withdraw", "log", "monitor", "account"]
BUSINESS_MENUS = ["dashboard", "customer", "novel", "invoice", "withdraw"]
SYSTEM_MENUS = ["log", "monitor", "account"]


def menus_for(role: str, menus: str):
    # super（仅 yy）：全部菜单；admin：业务菜单，无系统菜单；user：按勾选
    if role == "super":
        return ALL_MENUS
    if role == "admin":
        return BUSINESS_MENUS
    return [m for m in (menus or "").split(",") if m]


def client_login(db: Session, phone: str, password: str):
    cust = db.query(Customer).filter(Customer.phone == phone).first()
    if not cust or not cust.is_active:
        return None
    ok = verify_password(password, cust.password_hash) or password == build_client_default_password(phone)
    if not ok:
        return None
    token = create_access_token(str(cust.id), "client", settings.JWT_EXPIRE_MINUTES_CLIENT,
                                extra={"phone": cust.phone, "name": cust.customer_name})
    return {"access_token": token, "token_type": "Bearer",
            "expires_in": settings.JWT_EXPIRE_MINUTES_CLIENT * 60,
            "role": "client", "subject": str(cust.id),
            "customer_name": cust.customer_name, "phone": cust.phone}


def admin_login(db: Session, username: str, password: str):
    a = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not a or not a.is_active or not verify_password(password, a.password_hash):
        return None
    a.last_login_at = datetime.utcnow()
    db.commit()
    token = create_access_token(str(a.id), "admin", settings.JWT_EXPIRE_MINUTES_ADMIN,
                                extra={"username": a.username, "name": a.real_name})
    return {"access_token": token, "token_type": "Bearer",
            "expires_in": settings.JWT_EXPIRE_MINUTES_ADMIN * 60,
            "role": a.role, "subject": str(a.id),
            "username": a.username, "real_name": a.real_name,
            "menus": menus_for(a.role, a.menus)}
