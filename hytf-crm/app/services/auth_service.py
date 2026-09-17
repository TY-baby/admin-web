from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import build_client_default_password, create_access_token, verify_password
from app.models.admin_user import AdminUser
from app.models.customer import Customer


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
            "role": "admin", "subject": str(a.id),
            "username": a.username, "real_name": a.real_name}