from fastapi import APIRouter
from .live_chat import router as live_chat_router

router = APIRouter()
router.include_router(live_chat_router, prefix="/live-chat", tags=["live-chat"])