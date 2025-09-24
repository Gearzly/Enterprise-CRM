"""
DEPRECATED: JWT-based authentication middleware
This file has been replaced by OAuth 2.0 PKCE authentication middleware.
Use app.core.auth.oauth2_middleware instead.

MIGRATED TO: OAuth 2.0 with PKCE for enhanced security
- Better protection against token attacks
- No secret keys required (public key cryptography)
- Built-in PKCE protection against code injection
- Proper token revocation support

See: app.core.auth.oauth2_middleware for the new implementation
"""

# This file is deprecated and should not be used
# Import the new OAuth2 PKCE implementation instead
from ..auth.oauth2_middleware import (
    OAuth2AuthenticationMiddleware,
    OAuth2AuthorizationMiddleware,
    get_current_user,
    get_current_active_user,
    require_permissions,
    Permission,
    Role
)

# For backwards compatibility, re-export the new classes
AuthenticationMiddleware = OAuth2AuthenticationMiddleware
AuthorizationMiddleware = OAuth2AuthorizationMiddleware

# Log deprecation warning
import logging
logger = logging.getLogger(__name__)
logger.warning(
    "JWT authentication middleware is deprecated. "
    "Use OAuth2AuthenticationMiddleware from app.core.auth.oauth2_middleware instead."
)

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
    
    # Core permissions
    AUDIT_VIEW = "audit:view"
    COMPLIANCE_MANAGE = "compliance:manage"
    SECURITY_MANAGE = "security:manage"


class Role(Enum):
    """Define system roles with associated permissions"""
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    SALES_MANAGER = "sales_manager"
    SALES_REP = "sales_rep"
    MARKETING_MANAGER = "marketing_manager"
    MARKETING_SPECIALIST = "marketing_specialist"
    SUPPORT_MANAGER = "support_manager"
    SUPPORT_AGENT = "support_agent"
    USER = "user"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.SUPERADMIN: [
        Permission.SUPERADMIN_READ, Permission.SUPERADMIN_WRITE, Permission.SUPERADMIN_DELETE,
        Permission.USER_MANAGEMENT, Permission.SYSTEM_CONFIG,
        Permission.SALES_READ, Permission.SALES_WRITE, Permission.SALES_DELETE,
        Permission.MARKETING_READ, Permission.MARKETING_WRITE, Permission.MARKETING_DELETE,
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE, Permission.SUPPORT_DELETE,
        Permission.AUDIT_VIEW, Permission.COMPLIANCE_MANAGE, Permission.SECURITY_MANAGE
    ],
    Role.ADMIN: [
        Permission.USER_MANAGEMENT,
        Permission.SALES_READ, Permission.SALES_WRITE,
        Permission.MARKETING_READ, Permission.MARKETING_WRITE,
        Permission.SUPPORT_READ, Permission.SUPPORT_WRITE,
        Permission.AUDIT_VIEW
    ],
    Role.SALES_MANAGER: [
        Permission.SALES_READ, Permission.SALES_WRITE, Permission.SALES_DELETE,
        Permission.LEADS_MANAGE, Permission.OPPORTUNITIES_MANAGE, Permission.ACCOUNTS_MANAGE,
        Permission.REPORTS_VIEW
    ],
    Role.SALES_REP: [
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


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Centralized authentication middleware"""
    
    def __init__(self, app, exclude_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/openapi.json",
            "/api/superadmin/security/auth/token",
            "/api/superadmin/security/auth/register",
            "/favicon.ico",
            "/health",
            "/",
        ]
        self.security = HTTPBearer(auto_error=False)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process authentication for each request"""
        
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Extract token from request
        try:
            credentials = await self._extract_token(request)
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Validate token and get user
            user = await self._validate_token(credentials.credentials)
            
            # Add user to request state
            request.state.user = user
            request.state.authenticated = True
            
            logger.info(f"Authenticated user {user.email} for {request.method} {request.url.path}")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        response = await call_next(request)
        return response
    
    async def _extract_token(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """Extract Bearer token from request"""
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                return None
            return HTTPAuthorizationCredentials(scheme=scheme, credentials=token)
        except ValueError:
            return None
    
    async def _validate_token(self, token: str) -> User:
        """Validate JWT token and return user"""
        if not SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT secret key not configured"
            )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            # Get user from database
            user = get_user_by_email(email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            # Check if user is active
            if user.status != "active":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is inactive"
                )
            
            return user
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Role-based access control middleware"""
    
    def __init__(self, app, endpoint_permissions: Optional[Dict[str, List[Permission]]] = None):
        super().__init__(app)
        self.endpoint_permissions = endpoint_permissions or self._default_endpoint_permissions()
    
    def _default_endpoint_permissions(self) -> Dict[str, List[Permission]]:
        """Define default permissions for endpoints"""
        return {
            # SuperAdmin endpoints
            "/api/superadmin/users": [Permission.USER_MANAGEMENT],
            "/api/superadmin/system": [Permission.SYSTEM_CONFIG],
            "/api/superadmin/security": [Permission.SECURITY_MANAGE],
            
            # Sales endpoints
            "/api/sales/leads": [Permission.LEADS_MANAGE],
            "/api/sales/opportunities": [Permission.OPPORTUNITIES_MANAGE],
            "/api/sales/accounts": [Permission.ACCOUNTS_MANAGE],
            "/api/sales/reports": [Permission.REPORTS_VIEW],
            
            # Marketing endpoints
            "/api/marketing/campaigns": [Permission.CAMPAIGNS_MANAGE],
            "/api/marketing/email": [Permission.EMAIL_SEND],
            "/api/marketing/analytics": [Permission.ANALYTICS_VIEW],
            
            # Support endpoints
            "/api/support/tickets": [Permission.TICKETS_MANAGE],
            "/api/support/knowledge-base": [Permission.KNOWLEDGE_BASE_MANAGE],
            
            # Core endpoints
            "/api/core/audit": [Permission.AUDIT_VIEW],
            "/api/core/compliance": [Permission.COMPLIANCE_MANAGE],
            "/api/core/security": [Permission.SECURITY_MANAGE],
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check permissions for each request"""
        
        # Skip authorization for unauthenticated requests (handled by AuthenticationMiddleware)
        if not hasattr(request.state, 'user') or not request.state.authenticated:
            return await call_next(request)
        
        user = request.state.user
        
        # Check permissions for this endpoint
        required_permissions = self._get_required_permissions(request.url.path, request.method)
        
        if required_permissions:
            user_permissions = self._get_user_permissions(user)
            
            if not self._has_required_permissions(user_permissions, required_permissions):
                logger.warning(
                    f"Access denied for user {user.email} to {request.method} {request.url.path}. "
                    f"Required: {[p.value for p in required_permissions]}, "
                    f"User has: {[p.value for p in user_permissions]}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            logger.info(f"Access granted for user {user.email} to {request.method} {request.url.path}")
        
        response = await call_next(request)
        return response
    
    def _get_required_permissions(self, path: str, method: str) -> List[Permission]:
        """Get required permissions for an endpoint"""
        for endpoint_pattern, permissions in self.endpoint_permissions.items():
            if path.startswith(endpoint_pattern):
                # Adjust permissions based on HTTP method
                if method in ["GET", "HEAD"]:
                    # For read operations, check for read permission
                    read_perms = [p for p in permissions if p.value.endswith(":read")]
                    return read_perms if read_perms else permissions
                elif method in ["POST", "PUT", "PATCH"]:
                    # For write operations, check for write permission
                    write_perms = [p for p in permissions if p.value.endswith(":write")]
                    return write_perms if write_perms else permissions
                elif method == "DELETE":
                    # For delete operations, check for delete permission
                    delete_perms = [p for p in permissions if p.value.endswith(":delete")]
                    return delete_perms if delete_perms else permissions
                else:
                    return permissions
        
        return []  # No specific permissions required
    
    def _get_user_permissions(self, user: User) -> List[Permission]:
        """Get permissions for a user based on their role"""
        try:
            user_role = Role(user.role)
            return ROLE_PERMISSIONS.get(user_role, [])
        except ValueError:
            logger.warning(f"Unknown role for user {user.email}: {user.role}")
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
    """Get current authenticated user"""
    if not hasattr(request.state, 'user') or not request.state.authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if current_user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


def require_permissions(*permissions: Permission):
    """Decorator to require specific permissions for a route"""
    def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        user_permissions = AuthorizationMiddleware(None)._get_user_permissions(current_user)
        
        for permission in permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {permission.value}"
                )
        
        return current_user
    
    return permission_checker


def require_role(*roles: Role):
    """Decorator to require specific roles for a route"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        try:
            user_role = Role(current_user.role)
            if user_role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role required: {[r.value for r in roles]}"
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role"
            )
        
        return current_user
    
    return role_checker


# Utility functions
def is_superadmin(user: User) -> bool:
    """Check if user is a superadmin"""
    return user.role == Role.SUPERADMIN.value


def has_permission(user: User, permission: Permission) -> bool:
    """Check if user has a specific permission"""
    auth_middleware = AuthorizationMiddleware(None)
    user_permissions = auth_middleware._get_user_permissions(user)
    return permission in user_permissions


def get_user_role(user: User) -> Optional[Role]:
    """Get user's role enum"""
    try:
        return Role(user.role)
    except ValueError:
        return None