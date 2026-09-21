from datetime import datetime
from sqlalchemy import String, DateTime, Integer, DECIMAL, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Invoice(Base):
    __tablename__ = "t_invoice"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(50), default="")
    douyin_id: Mapped[str] = mapped_column(String(50), default="")
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(SAEnum("PENDING", "PROCESSED", name="invoice_status"), default="PENDING")
    invoice_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    remark: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)