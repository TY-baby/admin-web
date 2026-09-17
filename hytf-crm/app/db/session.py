from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_engine(settings.sqlalchemy_uri, pool_size=settings.MYSQL_POOL_SIZE,
                       max_overflow=settings.MYSQL_MAX_OVERFLOW, pool_pre_ping=True,
                       pool_recycle=3600, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

from app.models import admin_user, customer, douyin_account, finance_log, invoice  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)