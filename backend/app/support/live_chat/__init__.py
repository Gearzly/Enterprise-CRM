from fastapi import APIRouter
from .live_chat import router as live_chat_router

router = live_chat_router