import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.api import router, RequestMiddleware
from app.core.maintenance import setup_maintenance_middleware
from app.core.middleware import SecurityMiddleware
from config import get_settings, setup_logging
import os

settings = get_settings()
logger = setup_logging(settings.LOG_LEVEL)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Claude MCP Server",
        description="Machine Conversation Protocol Server with Recorded Future Integration",
        version=settings.VERSION,
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc"
    )

    # エラーハンドラーの追加
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"バリデーションエラー: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": "リクエストデータが無効です",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"HTTPエラー: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"予期せぬエラー: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "内部サーバーエラーが発生しました"
            }
        )

    # ミドルウェアの設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestMiddleware)

    # セキュリティミドルウェアの追加
    app.add_middleware(SecurityMiddleware)

    # メンテナンスモードの設定
    setup_maintenance_middleware(app)

    # ルーターの追加
    app.include_router(router)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.ENVIRONMENT == "development"
    )
