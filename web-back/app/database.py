import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

if settings.DB_TYPE == "sqlite":
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(retries: int = 20, delay: int = 3) -> bool:
    if settings.DB_TYPE == "sqlite":
        print("[DB] sqlite mode, skip waiting")
        return True
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("[DB] connected")
            return True
        except Exception as e:
            print(f"[DB] retry {i + 1}/{retries}: {e}")
            time.sleep(delay)
    return False