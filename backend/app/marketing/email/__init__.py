from fastapi import APIRouter
from .email import router as email_router

router = APIRouter()
router.include_router(email_router, prefix="/email", tags=["email"])