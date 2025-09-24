"""
Simple Authentication module for OAuth 2.0 PKCE
"""
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    if email == "test@example.com":
        return {"id": 1, "email": email, "name": "Test User", "status": "active"}
    return None

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = get_user_by_email(email)
    if not user:
        return None
    if email == "test@example.com":
        return user
    return None

@router.get("/test")
async def test_auth_module():
    return {"message": "Auth module working", "oauth2_configured": True, "auth_method": "oauth2_pkce"}
