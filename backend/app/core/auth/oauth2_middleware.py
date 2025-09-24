"""
OAuth 2.0 with PKCE Authentication Middleware
Replaces JWT-based authentication with OAuth 2.0 PKCE flow

This middleware:
1. Validates OAuth 2.0 access tokens
2. Enforces role-based access control
3. Provides centralized authentication across all endpoints
4. Implements proper token validation and user resolution
"""
import logging
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
from enum import Enum

from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .oauth2_pkce import oauth2_manager
from ...superadmin.models import User
from ..services.user_service import user_service

logger = logging.getLogger(__name__)


class Permission(Enum):
    """Define system permissions"""
    # SuperAdmin permissions
    SUPERADMIN_READ = "superadmin:read"
    SUPERADMIN_WRITE = "superadmin:write"
    SUPERADMIN_DELETE = "superadmin:delete"
    USER_MANAGEMENT = "users:manage"
    SYSTEM_CONFIG = "system:config"
    
    # Sales permissions
    SALES_READ = "sales:read"
    SALES_WRITE = "sales:write"
    SALES_DELETE = "sales:delete"
    LEADS_MANAGE = "leads:manage"
    OPPORTUNITIES_MANAGE = "opportunities:manage"
    ACCOUNTS_MANAGE = "accounts:manage"
    REPORTS_VIEW = "reports:view"
    
    # Marketing permissions
    MARKETING_READ = "marketing:read"
    MARKETING_WRITE = "marketing:write"
    MARKETING_DELETE = "marketing:delete"
    CAMPAIGNS_MANAGE = "campaigns:manage"
    EMAIL_SEND = "email:send"
    ANALYTICS_VIEW = "analytics:view"
    
    # Support permissions
    SUPPORT_READ = "support:read"
    SUPPORT_WRITE = "support:write"
    SUPPORT_DELETE = "support:delete"
    TICKETS_MANAGE = "tickets:manage"
    KNOWLEDGE_BASE_MANAGE = "kb:manage"


class Role(Enum):
    """Define user roles"""
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    SALES_MANAGER = "sales_manager"
    SALES_REPRESENTATIVE = "sales_rep"
    MARKETING_MANAGER = "marketing_manager"
    MARKETING_SPECIALIST = "marketing_specialist"
    SUPPORT_MANAGER = "support_manager"
    SUPPORT_AGENT = "support_agent"
    USER = "user"


# Role-based permissions mapping
ROLE_PERMISSIONS: Dict[Role, List[Permission]] = {
    Role.SUPERADMIN: [
        # Full system access
        Permission.SUPERADMIN_READ, Permission.SUPERADMIN_WRITE, Permission.SUPERADMIN_DELETE,
        Permission.USER_MANAGEMENT, Permission.SYSTEM_CONFIG,
        Permission.SALES_READ, Permission.SALES_WRITE, Permission.SALES_DELETE,
        Permission.LEADS_MANAGE, Permission.OPPORTUNITIES_MANAGE, Permission.ACCOUNTS_MANAGE,
        Permission.REPORTS_VIEW,
        Permission.MARKETING_READ, Permission.MARKETING_WRITE, Permission.MARKETING_DELETE,
        Permission.CAMPAIGNS_MANAGE, Permission.EMAIL_SEND, Permission.ANALYTICS_VIEW,
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE, Permission.SUPPORT_DELETE,
        Permission.TICKETS_MANAGE, Permission.KNOWLEDGE_BASE_MANAGE
    ],
    Role.ADMIN: [
        Permission.USER_MANAGEMENT,
        Permission.SALES_READ, Permission.SALES_WRITE,
        Permission.LEADS_MANAGE, Permission.OPPORTUNITIES_MANAGE, Permission.ACCOUNTS_MANAGE,
        Permission.REPORTS_VIEW,
        Permission.MARKETING_READ, Permission.MARKETING_WRITE,
        Permission.CAMPAIGNS_MANAGE, Permission.ANALYTICS_VIEW,
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE,
        Permission.TICKETS_MANAGE, Permission.KNOWLEDGE_BASE_MANAGE
    ],
    Role.SALES_MANAGER: [
        Permission.SALES_READ, Permission.SALES_WRITE, Permission.SALES_DELETE,
        Permission.LEADS_MANAGE, Permission.OPPORTUNITIES_MANAGE, Permission.ACCOUNTS_MANAGE,
        Permission.REPORTS_VIEW
    ],
    Role.SALES_REPRESENTATIVE: [
        Permission.SALES_READ, Permission.SALES_WRITE,
        Permission.LEADS_MANAGE, Permission.OPPORTUNITIES_MANAGE
    ],
    Role.MARKETING_MANAGER: [
        Permission.MARKETING_READ, Permission.MARKETING_WRITE, Permission.MARKETING_DELETE,
        Permission.CAMPAIGNS_MANAGE, Permission.EMAIL_SEND, Permission.ANALYTICS_VIEW
    ],
    Role.MARKETING_SPECIALIST: [
        Permission.MARKETING_READ, Permission.MARKETING_WRITE,
        Permission.CAMPAIGNS_MANAGE, Permission.EMAIL_SEND
    ],
    Role.SUPPORT_MANAGER: [
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE, Permission.SUPPORT_DELETE,
        Permission.TICKETS_MANAGE, Permission.KNOWLEDGE_BASE_MANAGE
    ],
    Role.SUPPORT_AGENT: [
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE,
        Permission.TICKETS_MANAGE
    ],
    Role.USER: [
        # Basic user permissions
    ]
}


class OAuth2AuthenticationMiddleware(BaseHTTPMiddleware):
    """OAuth 2.0 PKCE Authentication Middleware"""
    
    def __init__(self, app, exclude_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/openapi.json",
            "/auth/challenge",
            "/auth/authorize",
            "/auth/token",
            "/auth/callback",
            "/favicon.ico",
            "/health",
            "/",
        ]
        self.security = HTTPBearer(auto_error=False)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process OAuth 2.0 authentication for each request"""
        
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Extract token from request
        try:
            credentials = await self._extract_token(request)
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="OAuth 2.0 access token required",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Validate OAuth 2.0 access token
            token_data = await self._validate_oauth2_token(credentials.credentials)
            
            # Get user from token data
            user = await self._get_user_from_token(token_data)
            
            # Add user and token info to request state
            request.state.user = user
            request.state.token_data = token_data
            request.state.authenticated = True
            
            logger.info(f"OAuth2 authenticated user {user.email} for {request.method} {request.url.path}")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"OAuth2 authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OAuth 2.0 authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        response = await call_next(request)
        return response
    
    async def _extract_token(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """Extract OAuth 2.0 access token from request"""
        # Try Authorization header first
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ", 1)[1]
            return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        # Try query parameter as fallback
        token = request.query_params.get("access_token")
        if token:
            return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        return None
    
    async def _validate_oauth2_token(self, token: str) -> Dict[str, Any]:
        """Validate OAuth 2.0 access token"""
        token_data = oauth2_manager.validate_access_token(token)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired OAuth 2.0 access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_data
    
    async def _get_user_from_token(self, token_data: Dict[str, Any]) -> User:
        """Get user from token data"""
        user_id = token_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        # Get user by email from the user service
        user = user_service.get_user_by_email(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user


class OAuth2AuthorizationMiddleware(BaseHTTPMiddleware):
    """OAuth 2.0 Authorization Middleware (Role-based access control)"""
    
    def __init__(self, app):
        super().__init__(app)
        # Define path-based permission requirements
        self.path_permissions = {
            "/sales": [Permission.SALES_READ],
            "/marketing": [Permission.MARKETING_READ],
            "/support": [Permission.SUPPORT_READ],
            "/api/superadmin": [Permission.SUPERADMIN_READ],
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Enforce role-based authorization"""
        
        # Skip if not authenticated
        if not hasattr(request.state, 'authenticated') or not request.state.authenticated:
            return await call_next(request)
        
        # Get required permissions for the path
        required_permissions = self._get_required_permissions(request.url.path, request.method)
        
        if required_permissions:
            user = request.state.user
            user_permissions = self._get_user_permissions(user)
            
            if not self._has_required_permissions(user_permissions, required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions for this resource"
                )
        
        response = await call_next(request)
        return response
    
    def _get_required_permissions(self, path: str, method: str) -> List[Permission]:
        """Get required permissions for a path and method"""
        # Check for exact path matches first
        for path_pattern, permissions in self.path_permissions.items():
            if path.startswith(path_pattern):
                # Adjust permissions based on HTTP method
                if method in ["POST", "PUT", "PATCH"]:
                    # Write operations require write permissions
                    write_permissions = []
                    for perm in permissions:
                        if perm.value.endswith(":read"):
                            write_perm_name = perm.value.replace(":read", ":write")
                            # Find corresponding write permission
                            for write_perm in Permission:
                                if write_perm.value == write_perm_name:
                                    write_permissions.append(write_perm)
                                    break
                        else:
                            write_permissions.append(perm)
                    return write_permissions
                elif method == "DELETE":
                    # Delete operations require delete permissions
                    delete_permissions = []
                    for perm in permissions:
                        if perm.value.endswith(":read"):
                            delete_perm_name = perm.value.replace(":read", ":delete")
                            # Find corresponding delete permission
                            for delete_perm in Permission:
                                if delete_perm.value == delete_perm_name:
                                    delete_permissions.append(delete_perm)
                                    break
                        else:
                            delete_permissions.append(perm)
                    return delete_permissions
                else:
                    # GET and other read operations
                    return permissions
        
        return []
    
    def _get_user_permissions(self, user: User) -> List[Permission]:
        """Get user permissions based on role"""
        # In a real implementation, this would check user roles from database
        # For now, assume all users are admins for testing
        user_role = getattr(user, 'role', Role.USER.value)
        
        try:
            role_enum = Role(user_role)
            return ROLE_PERMISSIONS.get(role_enum, [])
        except ValueError:
            return []
    
    def _has_required_permissions(self, user_permissions: List[Permission],
                                required_permissions: List[Permission]) -> bool:
        """Check if user has all required permissions"""
        if not required_permissions:
            return True  # No permissions required
        
        for required_perm in required_permissions:
            if required_perm not in user_permissions:
                return False
        
        return True


# Dependency functions for FastAPI routes
async def get_current_user(request: Request) -> User:
    """Get current authenticated user from OAuth 2.0 token"""
    if not hasattr(request.state, 'user') or not request.state.authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth 2.0 authentication required"
        )
    return request.state.user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if hasattr(current_user, 'status') and current_user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


def require_permissions(*permissions: Permission):
    """Decorator to require specific permissions for an endpoint"""
    def permission_checker(request: Request) -> bool:
        if not hasattr(request.state, 'user') or not request.state.authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user = request.state.user
        user_permissions = OAuth2AuthorizationMiddleware(None)._get_user_permissions(user)
        
        for required_perm in permissions:
            if required_perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {required_perm.value}"
                )
        
        return True
    
    return Depends(permission_checker)


# OAuth 2.0 Security scheme for OpenAPI documentation
oauth2_scheme = HTTPBearer(
    scheme_name="OAuth2Bearer",
    description="OAuth 2.0 with PKCE authentication. Use 'Bearer <access_token>' format."
)