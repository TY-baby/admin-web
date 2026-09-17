from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Customer(Base):
    __tablename__ = "t_customer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_uid: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(50), default="")
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    remark: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)