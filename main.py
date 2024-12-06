import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router, RequestMiddleware
from app.core.maintenance import setup_maintenance_middleware
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

    # ミドルウェアの設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestMiddleware)

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
