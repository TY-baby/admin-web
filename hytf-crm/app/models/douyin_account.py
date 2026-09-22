from datetime import datetime
from sqlalchemy import String, DateTime, Integer, DECIMAL, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class DouyinAccount(Base):
    __tablename__ = "t_douyin_account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    douyin_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    douyin_name: Mapped[str] = mapped_column(String(50), default="")
    auto_code: Mapped[str] = mapped_column(String(6), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(20), default="")
    recharge_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    balance: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False, default=0)
    tier: Mapped[str] = mapped_column(SAEnum("A", "B", "C", name="tier_enum"), nullable=True, default=None)
    tier_daily_budget: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    launch_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    auth_start_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    auth_end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(SAEnum("NORMAL", "DISABLED", name="account_status"), default="NORMAL")
    remark: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)