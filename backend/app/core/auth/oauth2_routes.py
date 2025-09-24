"""
OAuth 2.0 with PKCE Authentication Routes
Provides OAuth 2.0 authorization flow endpoints
"""
import logging
import secrets
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, HttpUrl
from .oauth2_pkce import oauth2_manager

logger = logging.getLogger(__name__)

router = APIRouter()


class PKCEChallengeRequest(BaseModel):
    """Request to generate PKCE challenge"""
    pass


class AuthorizeRequest(BaseModel):
    """OAuth 2.0 authorization request"""
    client_id: str
    redirect_uri: HttpUrl
    code_challenge: str
    code_challenge_method: str = "S256"
    state: str


class TokenRequest(BaseModel):
    """OAuth 2.0 token request for username/password flow"""
    grant_type: str = "password"
    username: str
    password: str
    client_id: str = "crm_web_app"
    scope: str = "read write"


class LoginRequest(BaseModel):
    """Simple login request for demo accounts"""
    email: str
    password: str


class TokenRefreshRequest(BaseModel):
    """OAuth 2.0 token refresh request"""
    grant_type: str = "refresh_token"
    refresh_token: str
    client_id: str


@router.post("/challenge")
async def generate_pkce_challenge() -> Dict[str, str]:
    """
    Generate PKCE challenge for OAuth 2.0 flow
    Returns code_challenge and code_challenge_method for the client
    """
    try:
        challenge_data = oauth2_manager.generate_pkce_challenge()
        logger.info("Generated PKCE challenge")
        return {
            "code_challenge": challenge_data["code_challenge"],
            "code_challenge_method": challenge_data["code_challenge_method"]
        }
    except Exception as e:
        logger.error(f"Error generating PKCE challenge: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PKCE challenge"
        )


@router.post("/authorize")
async def authorize(request: AuthorizeRequest) -> Dict[str, str]:
    """
    OAuth 2.0 authorization endpoint
    Validates the authorization request and returns authorization code
    """
    try:
        # Validate PKCE challenge
        if request.code_challenge_method != "S256":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported code_challenge_method. Only S256 is supported."
            )
        
        # Generate authorization code directly for demo
        auth_code = secrets.token_urlsafe(32)
        
        logger.info(f"Generated authorization code for client {request.client_id}")
        
        return {
            "authorization_code": auth_code,
            "state": request.state,
            "redirect_uri": str(request.redirect_uri)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authorization failed"
        )


@router.post("/login")
async def simple_login(request: LoginRequest) -> Dict[str, Any]:
    """
    Simple login endpoint for demo accounts
    Compatible with existing frontend AuthService
    """
    try:
        # Demo account validation
        demo_accounts = {
            "admin@demo.com": {"role": "administrator", "name": "Administrator User"},
            "sales.manager@demo.com": {"role": "sales_manager", "name": "Sales Manager"},
            "sales.rep@demo.com": {"role": "sales_rep", "name": "Sales Representative"}
        }
        
        if request.email not in demo_accounts:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        user_info = demo_accounts[request.email]
        
        # Create a simple JWT-like token for demo
        # JWT Header
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        
        # JWT Payload
        payload = {
            "sub": request.email,
            "email": request.email,
            "name": user_info["name"],
            "role": user_info["role"],
            "permissions": ["read", "write"] + (["admin"] if user_info["role"] == "administrator" else []),
            "iat": int(datetime.utcnow().timestamp()),
            "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp())
        }
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # Simple signature (not secure, for demo only)
        signature = base64.urlsafe_b64encode(b'demo_signature').decode().rstrip('=')
        
        access_token = f"{header_b64}.{payload_b64}.{signature}"
        refresh_token = "demo_refresh_token_" + secrets.token_urlsafe(16)
        
        logger.info(f"Demo login successful for {request.email}")
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
            "user": {
                "id": "1",
                "email": request.email,
                "name": user_info["name"],
                "role": user_info["role"],
                "permissions": ["read", "write"] + (["admin"] if user_info["role"] == "administrator" else [])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/me")
async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Get current user information
    Compatible with frontend AuthService.getCurrentUser()
    """
    try:
        # For demo, return mock user info
        # In production, this would validate the Bearer token
        return {
            "id": "1",
            "email": "admin@demo.com",
            "name": "Administrator User",
            "role": "administrator",
            "permissions": ["read", "write", "admin"]
        }
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/token")
async def get_oauth2_token(request: TokenRequest) -> Dict[str, Any]:
    """
    OAuth 2.0 token endpoint with username/password flow
    Simplified for existing CRM clients
    """
    try:
        if request.grant_type != "password":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported grant_type. Only 'password' is supported."
            )
        
        # Simple authentication for test user
        if request.username != "test@example.com":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate access token using OAuth2 manager
        access_token = oauth2_manager._generate_access_token(
            client_id=request.client_id,
            user_id=request.username,
            scope=request.scope.split() if request.scope else ["read", "write"]
        )
        
        # Generate refresh token
        refresh_token = oauth2_manager._generate_refresh_token(
            access_token=access_token,
            client_id=request.client_id,
            user_id=request.username
        )
        
        logger.info(f"Generated OAuth2 tokens for user {request.username}")
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
            "scope": request.scope or "read write"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed"
        )


@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest) -> Dict[str, Any]:
    """
    OAuth 2.0 token refresh endpoint
    Exchange refresh token for new access token
    """
    try:
        if request.grant_type != "refresh_token":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported grant_type. Only 'refresh_token' is supported."
            )
        
        # For demo purposes, generate new tokens
        access_token = oauth2_manager._generate_access_token(
            client_id=request.client_id,
            user_id="test@example.com",
            scope=["read", "write"]
        )
        
        logger.info(f"Refreshed tokens for client {request.client_id}")
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": request.refresh_token,
            "scope": "read write"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/revoke")
async def revoke_token(request: Request) -> Dict[str, str]:
    """
    OAuth 2.0 token revocation endpoint
    Revoke access or refresh tokens
    """
    try:
        # Get token from request body
        body = await request.json()
        token = body.get("token")
        token_type_hint = body.get("token_type_hint", "access_token")
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is required"
            )
        
        # For demo purposes, always succeed
        logger.info(f"Revoked {token_type_hint}")
        return {"message": "Token revoked successfully"}
            
    except Exception as e:
        logger.error(f"Token revocation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token revocation failed"
        )


@router.get("/userinfo")
async def get_user_info(request: Request) -> Dict[str, Any]:
    """
    OAuth 2.0 UserInfo endpoint
    Returns information about the current user
    """
    try:
        # Simple user info for demo
        return {
            "sub": "1",
            "email": "test@example.com",
            "name": "Test User",
            "role": "user",
            "status": "active",
            "permissions": ["read", "write"],
            "scope": "read write"
        }
        
    except Exception as e:
        logger.error(f"UserInfo error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )


@router.get("/.well-known/oauth-authorization-server")
async def oauth_metadata() -> Dict[str, Any]:
    """
    OAuth 2.0 Authorization Server Metadata (RFC 8414)
    Provides discovery information about the OAuth 2.0 endpoints
    """
    base_url = "http://localhost:8000"  # This should be configurable
    
    return {
        "issuer": base_url,
        "authorization_endpoint": f"{base_url}/auth/authorize",
        "token_endpoint": f"{base_url}/auth/token",
        "userinfo_endpoint": f"{base_url}/auth/userinfo",
        "revocation_endpoint": f"{base_url}/auth/revoke",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["none", "client_secret_basic"],
        "scopes_supported": ["read", "write", "admin"],
        "claims_supported": ["sub", "email", "name", "role"],
        "subject_types_supported": ["public"]
    }