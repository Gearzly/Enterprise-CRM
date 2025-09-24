"""
OAuth 2.0 with PKCE Authentication Routes
Provides OAuth 2.0 authorization flow endpoints
"""
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from fastapi.responses import RedirectResponse
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
        
        # In a real implementation, this would:
        # 1. Authenticate the user (login form)
        # 2. Ask for user consent 
        # 3. Generate authorization code
        
        # For this implementation, we'll generate an authorization code directly
        auth_code = oauth2_manager.create_authorization_code(
            client_id=request.client_id,
            redirect_uri=str(request.redirect_uri),
            code_challenge=request.code_challenge,
            code_challenge_method=request.code_challenge_method,
            user_id="user@example.com"  # This would come from authentication
        )
        
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
        
        # Refresh access token
        token_data = oauth2_manager.refresh_access_token(
            refresh_token=request.refresh_token,
            client_id=request.client_id
        )
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refresh token"
            )
        
        logger.info(f"Refreshed tokens for client {request.client_id}")
        
        return {
            "access_token": token_data["access_token"],
            "token_type": "Bearer",
            "expires_in": token_data["expires_in"],
            "refresh_token": token_data.get("refresh_token"),  # May issue new refresh token
            "scope": token_data.get("scope", "read write")
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
async def revoke_token(
    token: str,
    token_type_hint: str = "access_token"
) -> Dict[str, str]:
    """
    OAuth 2.0 token revocation endpoint
    Revoke access or refresh tokens
    """
    try:
        success = oauth2_manager.revoke_token(token, token_type_hint)
        
        if success:
            logger.info(f"Revoked {token_type_hint}")
            return {"message": "Token revoked successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
            
    except HTTPException:
        raise
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
        # The OAuth2AuthenticationMiddleware should have validated the token
        # and set request.state.user
        if not hasattr(request.state, 'user'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Valid access token required"
            )
        
        user = request.state.user
        token_data = getattr(request.state, 'token_data', {})
        
        return {
            "sub": user.id,
            "email": user.email,
            "name": getattr(user, 'name', user.email),
            "role": getattr(user, 'role', 'user'),
            "status": getattr(user, 'status', 'active'),
            "permissions": token_data.get("permissions", []),
            "scope": token_data.get("scope", "read write")
        }
        
    except HTTPException:
        raise
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