from fastapi import APIRouter
from .routes import router as main_router
from .admin import router as admin_router
from .middleware import RequestMiddleware

router = APIRouter()
router.include_router(main_router)
router.include_router(admin_router)

__all__ = ['router', 'RequestMiddleware']
