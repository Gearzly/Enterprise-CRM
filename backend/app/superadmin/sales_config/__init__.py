from fastapi import APIRouter
from .sales_config import router as sales_config_router

router = APIRouter(prefix="/sales-config", tags=["Sales Configuration"])
router.include_router(sales_config_router)