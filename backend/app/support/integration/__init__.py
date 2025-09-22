from fastapi import APIRouter
from .integration import router as integration_router

router = APIRouter()
router.include_router(integration_router, prefix="/integration", tags=["integration"])