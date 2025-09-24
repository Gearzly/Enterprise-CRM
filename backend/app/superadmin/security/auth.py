"""
Simple Authentication module for OAuth 2.0 PKCE
"""
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter
from passlib.context import CryptContext

# Add required FastAPI imports for endpoints
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

# Import the OAuth2 PKCE manager to generate and refresh tokens
from app.core.auth.oauth2_pkce import oauth2_manager
from app.core.services.user_service import user_service

logger = logging.getLogger(__name__)
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Defaults for demo/client compatibility
DEFAULT_CLIENT_ID = "crm_web_app"
DEFAULT_SCOPE = ["read", "write"]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email - delegates to user service"""
    return user_service.get_user_by_email(email)

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user - delegates to user service"""
    return user_service.authenticate_user(email, password)

# Helper function to get current user from request (avoiding circular import)
def get_current_user_from_request(request: Request) -> Dict[str, Any]:
    """Get current user from OAuth2 token in request headers."""
    # Extract token from Authorization header
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth 2.0 access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split(" ", 1)[1]
    
    # Validate token with OAuth2 manager
    token_data = oauth2_manager.validate_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OAuth 2.0 access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from token data
    user_id = token_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    
    user = get_user_by_email(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.get("/test")
async def test_auth_module():
    return {"message": "Auth module working", "oauth2_configured": True, "auth_method": "oauth2_pkce"}

# OAuth2 Password Grant-style token endpoint (form-encoded)
@router.post("/token")
async def issue_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """Issue OAuth2-style tokens for demo/testing via form-encoded credentials."""
    try:
        username = form_data.username
        password = form_data.password

        # Authenticate user using the user service
        user = user_service.authenticate_user(username, password)
        if not user:
            # Return Unauthorized for invalid credentials
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # Generate access and refresh tokens via the PKCE manager
        access_token = oauth2_manager._generate_access_token(
            client_id=DEFAULT_CLIENT_ID,
            user_id=username,
            scope=DEFAULT_SCOPE,
        )
        refresh_token = oauth2_manager._generate_refresh_token(
            access_token=access_token,
            client_id=DEFAULT_CLIENT_ID,
            user_id=username,
        )

        logger.info(f"Issued tokens for user {username}")
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
            "scope": " ".join(DEFAULT_SCOPE),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token issuance error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token issuance failed")

# Token refresh endpoint to rotate access/refresh tokens
class TokenRefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest) -> Dict[str, Any]:
    try:
        token_response = oauth2_manager.refresh_access_token(
            refresh_token=request.refresh_token,
            client_id=DEFAULT_CLIENT_ID,
        )
        # Convert dataclass to dict-like response
        response_body: Dict[str, Any] = {
            "access_token": token_response.access_token,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "refresh_token": token_response.refresh_token,
        }
        if token_response.scope:
            response_body["scope"] = token_response.scope
        return response_body
    except HTTPException:
        # Pass through expected errors (invalid/expired token)
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token refresh failed")

# Token revocation endpoint
class TokenRevokeRequest(BaseModel):
    token: str
    token_type_hint: Optional[str] = "access_token"

@router.post("/revoke")
async def revoke_token(request: TokenRevokeRequest) -> Dict[str, Any]:
    """Revoke an access token or refresh token."""
    try:
        # Use the oauth2_manager to revoke the token
        success = oauth2_manager.revoke_token(
            token=request.token,
            token_type=request.token_type_hint or "access_token"
        )
        
        if success:
            logger.info(f"Successfully revoked {request.token_type_hint} token")
            return {"message": "Token revoked successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token not found or already revoked"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token revocation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token revocation failed"
        )

# Current user endpoint (requires authentication)
@router.get("/me")
async def get_current_user_info(request: Request) -> Dict[str, Any]:
    """Get current user information using OAuth2 authentication."""
    try:
        current_user = get_current_user_from_request(request)
        return {
            "id": current_user.get('id', 1),
            "email": current_user.get('email', 'user@example.com'),
            "name": current_user.get('name', current_user.get('email', 'User')),
            "role": current_user.get('role', 'user'),
            "status": current_user.get('status', 'active'),
            "auth_method": "oauth2_pkce"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )
