from fastapi import APIRouter
from .modules import router as modules_router

router = APIRouter(prefix="/modules", tags=["Module Management"])
router.include_router(modules_router)