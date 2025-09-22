from fastapi import APIRouter
from .sla import router as sla_router

router = APIRouter()
router.include_router(sla_router, prefix="/sla", tags=["sla"])