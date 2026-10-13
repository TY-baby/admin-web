from datetime import datetime
from sqlalchemy import String, DateTime, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Withdraw(Base):
    __tablename__ = "t_withdraw"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    payee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    payee_card_no: Mapped[str] = mapped_column(String(50), default="")
    payee_bank_name: Mapped[str] = mapped_column(String(100), default="")
    payee_holder_name: Mapped[str] = mapped_column(String(60), default="")
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    customer_name: Mapped[str] = mapped_column(String(100), default="")
    douyin_account_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    douyin_id: Mapped[str] = mapped_column(String(50), default="")
    douyin_name: Mapped[str] = mapped_column(String(50), default="")
    launch_type: Mapped[str] = mapped_column(String(20), default="", index=True)
    generated_count: Mapped[int] = mapped_column(Integer, default=0)
    payable_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False, default=0)
    remark: Mapped[str] = mapped_column(String(255), default="")
    operator: Mapped[str] = mapped_column(String(50), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)