"""hytf-crm FastAPI 应用入口。"""
import time
from contextlib import asynccontextmanager

import psutil
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text

from app import __version__
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging_conf import logger
from app.core.security import hash_password
from app.db.redis_client import redis_client
from app.db.session import SessionLocal, engine, init_db
from app.middlewares.rate_limit import limiter
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.models.admin_user import AdminUser


def _bootstrap_admin():
    db = SessionLocal()
    try:
        if db.query(AdminUser).filter(AdminUser.username == "admin").first() is None:
            db.add(AdminUser(username="admin",
                             password_hash=hash_password("admin123"),
                             real_name="超级管理员", role="super"))
            db.commit()
            logger.info("[bootstrap] default admin created: admin / admin123")
    except Exception as e:
        logger.warning(f"[bootstrap] admin skipped: {e}")
    finally:
        db.close()


def _check_server_alerts():
    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        if cpu > settings.ALERT_CPU_THRESHOLD:
            logger.warning(f"[ALERT] CPU {cpu:.1f}% > {settings.ALERT_CPU_THRESHOLD}%")
        if mem > settings.ALERT_MEM_THRESHOLD:
            logger.warning(f"[ALERT] MEM {mem:.1f}% > {settings.ALERT_MEM_THRESHOLD}%")
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"[{settings.APP_NAME}] starting env={settings.APP_ENV} v={__version__}")
    if settings.APP_ENV == "dev":
        try:
            init_db()
            _bootstrap_admin()
            logger.info("[bootstrap] schema synced")
        except Exception as e:
            logger.error(f"[bootstrap] schema sync failed: {e}")
    try:
        redis_client.ping()
        logger.info("[bootstrap] redis ok")
    except Exception as e:
        logger.warning(f"[bootstrap] redis unavailable: {e}")
    yield
    engine.dispose()
    logger.info(f"[{settings.APP_NAME}] stopped")


app = FastAPI(title="hytf-crm API", version=__version__,
              description="恒耀引擎 CRM 后端",
              lifespan=lifespan,
              docs_url="/docs" if settings.APP_DEBUG else None,
              redoc_url=None)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=settings.CORS_ORIGINS or ["*"],
                   allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"],
                   expose_headers=["Content-Disposition"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.middleware("http")
async def access_log(request: Request, call_next):
    t0 = time.perf_counter()
    try:
        resp = await call_next(request)
    except Exception as e:
        logger.exception(f"[unhandled] path={request.url.path} err={e}")
        return JSONResponse(status_code=500,
                            content={"code": 500, "msg": "服务器内部错误", "data": None})
    ms = (time.perf_counter() - t0) * 1000
    try:
        key = f"qps:{int(time.time())}"
        cnt = redis_client.incr(key)
        if cnt == 1:
            redis_client.expire(key, 5)
        if cnt > settings.ALERT_QPS_THRESHOLD:
            logger.warning(f"[ALERT] QPS {cnt} > {settings.ALERT_QPS_THRESHOLD}")
    except Exception:
        pass
    _check_server_alerts()
    logger.info(f"{request.method} {request.url.path} -> {resp.status_code} {ms:.1f}ms")
    return resp


@app.get("/", tags=["health"])
def root():
    return {"code": 0, "msg": "ok",
            "data": {"app": settings.APP_NAME, "version": __version__, "docs": "/docs"}}


@app.get("/health", tags=["health"])
def health():
    db_ok, redis_ok = True, True
    try:
        s = SessionLocal(); s.execute(text("SELECT 1")); s.close()
    except Exception:
        db_ok = False
    try:
        redis_client.ping()
    except Exception:
        redis_ok = False
    return {"code": 0, "msg": "ok",
            "data": {"db": db_ok, "redis": redis_ok,
                     "cpu_percent": psutil.cpu_percent(interval=None),
                     "mem_percent": psutil.virtual_memory().percent}}


app.include_router(api_router, prefix="/api/v1")
