import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # sqlite = 本地开发零安装；mysql = 生产环境（Docker 默认走这个）
    DB_TYPE = os.getenv("DB_TYPE", "mysql")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "my_project")
    DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH", "./my_project.db")
    JWT_SECRET = os.getenv("JWT_SECRET", "my-project-secret-key-2026")
    JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "1440"))
    PORT = int(os.getenv("PORT", "8000"))

    @property
    def database_url(self) -> str:
        if self.DB_TYPE == "sqlite":
            return "sqlite:///" + self.DB_SQLITE_PATH
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )


settings = Settings()