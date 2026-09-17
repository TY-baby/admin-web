from datetime import datetime
from sqlalchemy import String, DateTime, Integer, DECIMAL, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class FinanceLog(Base):
    __tablename__ = "t_finance_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    douyin_account_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    change_type: Mapped[str] = mapped_column(SAEnum("RECHARGE", "CONSUME", "REFUND", "ADJUST", name="change_type"), nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    balance_after: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    stat_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    remark: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)