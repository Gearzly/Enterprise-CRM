from fastapi import APIRouter
from .security import router as security_router
from .auth import router as auth_router

router = APIRouter(prefix="/security", tags=["Security"])

router.include_router(security_router)
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])