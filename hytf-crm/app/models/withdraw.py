from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Withdraw(Base):
    __tablename__ = "t_withdraw"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    pay_date: Mapped[date] = mapped_column(Date, nullable=False)
    id_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payable_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False, default=0)
    remark: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)