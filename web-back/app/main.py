from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, wait_for_db
from . import seed
from .routers import auth, news, click, transaction

app = FastAPI(title="My Project API", version="1.0.0", description="网站推流点击追踪服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    if wait_for_db():
        try:
            Base.metadata.create_all(bind=engine)
            seed.init_data()
            print("[APP] database ready")
        except Exception as e:
            print(f"[APP] create tables failed (server still up): {e}")
    else:
        print("[APP] database unavailable, server still up")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "My Project API is running"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(click.router, prefix="/api/click", tags=["click"])
app.include_router(transaction.router, prefix="/api/transactions", tags=["transactions"])