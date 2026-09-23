from datetime import datetime
from sqlalchemy import String, DateTime, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class NovelPage(Base):
    __tablename__ = "t_novel_page"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    douyin_id: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    page_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    tier: Mapped[str] = mapped_column(String(1), nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)
    consumed: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False, default=0)
    reads_start: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reads_cap: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    seed: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    refresh_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)