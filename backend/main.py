from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.database import engine, Base
from app.api import auth, families, transactions, stats, ai, version, budgets, admin, v2
from app.utils.contracts import normalize_error_detail

V1_DEPRECATED_PREFIXES = (
    "/api/transactions",
    "/api/stats",
    "/api/ai",
    "/api/version",
    "/api/budgets",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    for _ in range(30):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except OperationalError:
            await asyncio.sleep(1)
    yield
    # 关闭时的清理工作
    pass

app = FastAPI(
    title="记账小助手后端服务",
    description="为记账小助手提供后端服务支持",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def v1_public_channel_guard(request: Request, call_next):
    if settings.ENABLE_V1_PUBLIC_API:
        return await call_next(request)

    if request.url.path.startswith(V1_DEPRECATED_PREFIXES):
        return JSONResponse(
            status_code=410,
            content={
                "message": "V1 公共接口已下线，请迁移到 V2 授权通道",
                "detail": "请改用 /api/v2/* 并携带 X-License-Code 完成授权调用"
            }
        )

    return await call_next(request)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(families.router, prefix="/api/families", tags=["家庭管理"])
if settings.ENABLE_V1_PUBLIC_API:
    app.include_router(transactions.router, prefix="/api/transactions", tags=["交易管理"])
    app.include_router(stats.router, prefix="/api/stats", tags=["统计分析"])
    app.include_router(ai.router, prefix="/api/ai", tags=["AI服务"])
    app.include_router(version.router, prefix="/api/version", tags=["版本管理"])
    app.include_router(budgets.router, prefix="/api/budgets", tags=["预算管理"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理后台"])
app.include_router(v2.router, prefix="/api/v2", tags=["授权通道V2"])

@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    detail = normalize_error_detail(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": detail,
            "detail": detail
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    detail = normalize_error_detail(exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "message": "请求参数校验失败",
            "detail": detail
        }
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "服务器内部错误",
            "detail": "服务器内部错误"
        }
    )

@app.get("/")
async def root():
    return {"message": "记账小助手后端服务", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
