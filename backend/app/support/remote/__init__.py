from fastapi import APIRouter
from .remote import router as remote_router

router = APIRouter()
router.include_router(remote_router, prefix="/remote", tags=["remote"])