from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "hytf-crm"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    APP_SECRET_KEY: str = "change-me"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_DB: str = "hytf_crm"
    MYSQL_POOL_SIZE: int = 10
    MYSQL_MAX_OVERFLOW: int = 20
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES_CLIENT: int = 720
    JWT_EXPIRE_MINUTES_ADMIN: int = 120
    RATE_LIMIT_LOGIN: str = "5/minute"
    RATE_LIMIT_API: str = "120/minute"
    ALERT_CPU_THRESHOLD: int = 80
    ALERT_MEM_THRESHOLD: int = 80
    ALERT_QPS_THRESHOLD: int = 200
    CORS_ORIGINS: List[str] = ["http://localhost:8081", "http://127.0.0.1:8081"]

    @property
    def sqlalchemy_uri(self) -> str:
        return (f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
                f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4")

    @property
    def redis_url(self) -> str:
        pwd = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{pwd}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()