from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    real_name = Column(String(64), default="")
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
        }


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    category = Column(String(64), default="公司新闻")
    summary = Column(String(500), default="")
    url = Column(String(500), default="")
    fee = Column(Float, default=0)
    cover = Column(String(500), default="")
    publish_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "summary": self.summary,
            "url": self.url,
            "fee": float(self.fee or 0),
            "cover": self.cover,
            "publish_time": self.publish_time.strftime("%Y-%m-%d %H:%M:%S")
            if self.publish_time else "",
        }


class ClickLog(Base):
    __tablename__ = "click_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, default=0, index=True)
    title = Column(String(255), default="", index=True)
    fee = Column(Float, default=0)
    url = Column(String(500), default="")
    ip = Column(String(64), default="")
    click_time = Column(DateTime, server_default=func.now(), index=True)