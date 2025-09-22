from fastapi import APIRouter
from .security import router as security_router

router = APIRouter(prefix="/security", tags=["Security Management"])
router.include_router(security_router)