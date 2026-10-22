from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.utils.timeutil import now_cn


class NovelPromo(Base):
    __tablename__ = "t_novel_promo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    customer_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=0)
    account_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=0)
    platform_code: Mapped[str] = mapped_column(String(30), default="")
    promo_content: Mapped[str] = mapped_column(String(20), default="")
    tier: Mapped[str] = mapped_column(String(1), default="A")
    base_reads: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    visits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_cn)