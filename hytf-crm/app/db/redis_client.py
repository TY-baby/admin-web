from typing import Optional
import redis
from app.core.config import settings

_pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True, max_connections=50)
redis_client = redis.Redis(connection_pool=_pool)


def cache_get(key: str) -> Optional[str]:
    try: return redis_client.get(key)
    except redis.RedisError: return None


def cache_set(key: str, value: str, ex: int = 300) -> None:
    try: redis_client.set(key, value, ex=ex)
    except redis.RedisError: pass