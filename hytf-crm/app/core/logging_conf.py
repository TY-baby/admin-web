import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="DEBUG" if settings.APP_DEBUG else "INFO",
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add(LOG_DIR / "app_{time:YYYY-MM-DD}.log", rotation="00:00", retention="14 days",
           level="INFO", encoding="utf-8", enqueue=True)
__all__ = ["logger"]