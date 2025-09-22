from fastapi import APIRouter
from .asset import router as asset_router

router = APIRouter()
router.include_router(asset_router, prefix="/asset", tags=["asset"])