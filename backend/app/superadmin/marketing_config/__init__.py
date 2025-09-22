from fastapi import APIRouter
from .marketing_config import router as marketing_config_router

router = APIRouter()
router.include_router(marketing_config_router, prefix="/marketing-config", tags=["marketing-config"])