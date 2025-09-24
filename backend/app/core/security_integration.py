"""
Comprehensive security and middleware integration for the CRM application.
This module ties together all security components, middleware, and configurations
to provide a unified, secure, and robust application architecture.
"""
import logging
import os
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Import all custom middleware and security components
from .middleware.error_handling import ErrorHandlingMiddleware, SecurityErrorMiddleware
from .middleware.auth_middleware import AuthenticationMiddleware, AuthorizationMiddleware
from .middleware.sanitization_middleware import (
    SecurityMiddleware, 
    SQLInjectionDetectionMiddleware, 
    RateLimitingMiddleware
)
from .security.rate_limiting import RateLimitMiddleware
from .session.redis_session import session_manager
from .database.session_manager import db_manager
from .memory.bounded_collections import memory_monitor
from ..superadmin.security.auth import router as auth_router

logger = logging.getLogger(__name__)


class SecurityConfig:
    """Centralized security configuration"""
    
    def __init__(self):
        # CORS settings
        self.allowed_origins = self._get_allowed_origins()
        self.allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allowed_headers = ["*"]
        self.allow_credentials = True
        
        # Trusted hosts
        self.trusted_hosts = self._get_trusted_hosts()
        
        # Security middleware settings
        self.enable_input_sanitization = os.getenv("ENABLE_INPUT_SANITIZATION", "true").lower() == "true"
        self.enable_security_headers = os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true"
        self.enable_rate_limiting = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        self.enable_sql_injection_detection = os.getenv("ENABLE_SQL_INJECTION_DETECTION", "true").lower() == "true"
        
        # Error handling
        self.include_traceback = os.getenv("INCLUDE_ERROR_TRACEBACK", "false").lower() == "true"
        
        # Authentication
        self.enforce_authentication = os.getenv("ENFORCE_AUTHENTICATION", "true").lower() == "true"
        self.enforce_authorization = os.getenv("ENFORCE_AUTHORIZATION", "true").lower() == "true"
        
        # Session management
        self.use_redis_sessions = os.getenv("USE_REDIS_SESSIONS", "true").lower() == "true"
    
    def _get_allowed_origins(self) -> List[str]:
        """Get allowed CORS origins from environment"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
        return [origin.strip() for origin in origins_str.split(",")]
    
    def _get_trusted_hosts(self) -> List[str]:
        """Get trusted hosts from environment"""
        hosts_str = os.getenv("TRUSTED_HOSTS", "localhost,127.0.0.1,*.example.com")
        return [host.strip() for host in hosts_str.split(",")]


def setup_security_middleware(app: FastAPI, config: SecurityConfig = None):
    """Setup all security middleware in the correct order"""
    if config is None:
        config = SecurityConfig()
    
    logger.info("Setting up comprehensive security middleware...")
    
    # 1. Trusted Host Middleware (first line of defense)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=config.trusted_hosts
    )
    
    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allowed_methods,
        allow_headers=config.allowed_headers,
    )
    
    # 3. Error Handling Middleware (high priority)
    app.add_middleware(
        ErrorHandlingMiddleware,
        include_traceback=config.include_traceback
    )
    
    # 4. Security Error Monitoring
    app.add_middleware(SecurityErrorMiddleware)
    
    # 5. Rate Limiting Middleware (before authentication)
    if config.enable_rate_limiting:
        app.add_middleware(RateLimitMiddleware)
    
    # 6. SQL Injection Detection (before input processing)
    if config.enable_sql_injection_detection:
        app.add_middleware(SQLInjectionDetectionMiddleware)
    
    # 7. Input Sanitization and Security Headers
    if config.enable_input_sanitization or config.enable_security_headers:
        app.add_middleware(
            SecurityMiddleware,
            enable_sanitization=config.enable_input_sanitization,
            enable_security_headers=config.enable_security_headers
        )
    
    # 8. Authentication Middleware
    if config.enforce_authentication:
        app.add_middleware(
            AuthenticationMiddleware,
            exclude_paths=[
                "/docs",
                "/openapi.json",
                "/api/superadmin/security/auth/token",
                "/api/superadmin/security/auth/register",
                "/favicon.ico",
                "/health",
                "/",
            ]
        )
    
    # 9. Authorization Middleware (after authentication)
    if config.enforce_authorization:
        app.add_middleware(AuthorizationMiddleware)
    
    logger.info("Security middleware setup completed")


def setup_health_checks(app: FastAPI):
    """Setup health check endpoints"""
    
    @app.get("/health")
    async def health_check():
        """Comprehensive health check"""
        health_status = {
            "status": "healthy",
            "timestamp": "2025-01-23T10:00:00Z",  # Would be dynamic in real implementation
            "checks": {}
        }
        
        # Database health
        try:
            db_healthy = db_manager.health_check()
            health_status["checks"]["database"] = {
                "status": "healthy" if db_healthy else "unhealthy",
                "details": db_manager.get_connection_pool_stats() if db_healthy else "Connection failed"
            }
        except Exception as e:
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Redis session health
        try:
            redis_healthy = session_manager.health_check()
            health_status["checks"]["redis_sessions"] = {
                "status": "healthy" if redis_healthy else "unhealthy",
                "details": session_manager.get_session_stats() if redis_healthy else "Connection failed"
            }
        except Exception as e:
            health_status["checks"]["redis_sessions"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Memory health
        try:
            memory_stats = memory_monitor.get_total_memory_usage()
            health_status["checks"]["memory"] = {
                "status": "healthy",
                "details": memory_stats
            }
        except Exception as e:
            health_status["checks"]["memory"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Overall status
        unhealthy_checks = [check for check in health_status["checks"].values() if check["status"] != "healthy"]
        if unhealthy_checks:
            health_status["status"] = "unhealthy"
        
        return health_status
    
    @app.get("/health/live")
    async def liveness_check():
        """Liveness probe for Kubernetes"""
        return {"status": "alive"}
    
    @app.get("/health/ready")
    async def readiness_check():
        """Readiness probe for Kubernetes"""
        # Check if all critical services are ready
        db_ready = db_manager.health_check()
        redis_ready = session_manager.health_check()
        
        if db_ready and redis_ready:
            return {"status": "ready"}
        else:
            return {"status": "not ready", "database": db_ready, "redis": redis_ready}


def setup_security_endpoints(app: FastAPI):
    """Setup security-related endpoints"""
    
    @app.get("/security/info")
    async def security_info():
        """Get security configuration information (non-sensitive)"""
        config = SecurityConfig()
        return {
            "cors_enabled": True,
            "trusted_hosts_configured": len(config.trusted_hosts) > 0,
            "input_sanitization_enabled": config.enable_input_sanitization,
            "rate_limiting_enabled": config.enable_rate_limiting,
            "authentication_enforced": config.enforce_authentication,
            "authorization_enforced": config.enforce_authorization,
            "redis_sessions_enabled": config.use_redis_sessions,
            "security_headers_enabled": config.enable_security_headers
        }
    
    # Include authentication router
    app.include_router(auth_router, prefix="/api/superadmin/security/auth", tags=["Authentication"])


def initialize_security_components():
    """Initialize all security components"""
    logger.info("Initializing security components...")
    
    # Initialize database manager
    try:
        db_stats = db_manager.get_connection_pool_stats()
        logger.info(f"Database manager initialized: {db_stats}")
    except Exception as e:
        logger.error(f"Failed to initialize database manager: {e}")
    
    # Initialize session manager
    try:
        session_stats = session_manager.get_session_stats()
        logger.info(f"Session manager initialized: {session_stats}")
    except Exception as e:
        logger.error(f"Failed to initialize session manager: {e}")
    
    # Initialize memory monitor
    try:
        memory_stats = memory_monitor.get_total_memory_usage()
        logger.info(f"Memory monitor initialized: {memory_stats}")
    except Exception as e:
        logger.error(f"Failed to initialize memory monitor: {e}")
    
    logger.info("Security components initialization completed")


def cleanup_security_components():
    """Cleanup all security components on shutdown"""
    logger.info("Cleaning up security components...")
    
    try:
        # Cleanup database connections
        db_manager.close_all_connections()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")
    
    try:
        # Cleanup memory caches
        memory_monitor.cleanup_all()
        logger.info("Memory caches cleaned up")
    except Exception as e:
        logger.error(f"Error cleaning up memory caches: {e}")
    
    logger.info("Security components cleanup completed")


def create_secure_app(
    title: str = "CRM API",
    description: str = "Comprehensive CRM System with Enterprise Security",
    version: str = "1.0.0"
) -> FastAPI:
    """Create a FastAPI application with comprehensive security"""
    
    # Create FastAPI app
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        docs_url="/docs" if os.getenv("ENABLE_DOCS", "true").lower() == "true" else None,
        redoc_url="/redoc" if os.getenv("ENABLE_REDOC", "true").lower() == "true" else None,
    )
    
    # Initialize security components
    initialize_security_components()
    
    # Setup middleware
    config = SecurityConfig()
    setup_security_middleware(app, config)
    
    # Setup health checks
    setup_health_checks(app)
    
    # Setup security endpoints
    setup_security_endpoints(app)
    
    # Setup shutdown handler
    @app.on_event("shutdown")
    async def shutdown_event():
        cleanup_security_components()
    
    logger.info(f"Secure FastAPI application created: {title} v{version}")
    
    return app


# Utility functions for manual security setup
def verify_security_configuration() -> dict:
    """Verify that all security components are properly configured"""
    results = {
        "environment_variables": {},
        "components": {},
        "recommendations": []
    }
    
    # Check environment variables
    required_env_vars = [
        "JWT_SECRET_KEY",
        "SECRET_ENCRYPTION_KEY", 
        "SESSION_SECRET_KEY",
        "DATABASE_URL",
        "REDIS_URL"
    ]
    
    for var in required_env_vars:
        value = os.getenv(var)
        results["environment_variables"][var] = {
            "configured": value is not None,
            "length": len(value) if value else 0,
            "secure": len(value) >= 32 if value else False
        }
        
        if not value:
            results["recommendations"].append(f"Set {var} environment variable")
        elif len(value) < 32:
            results["recommendations"].append(f"Use a longer {var} (minimum 32 characters)")
    
    # Check component health
    try:
        results["components"]["database"] = db_manager.health_check()
    except Exception as e:
        results["components"]["database"] = False
        results["recommendations"].append(f"Fix database connection: {e}")
    
    try:
        results["components"]["redis"] = session_manager.health_check()
    except Exception as e:
        results["components"]["redis"] = False
        results["recommendations"].append(f"Fix Redis connection: {e}")
    
    # Overall security score
    total_checks = len(required_env_vars) + len(results["components"])
    passed_checks = (
        sum(1 for check in results["environment_variables"].values() if check["configured"]) +
        sum(1 for check in results["components"].values() if check)
    )
    
    results["security_score"] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    results["overall_status"] = "secure" if results["security_score"] >= 90 else "needs_improvement"
    
    return results


# Export main functions
__all__ = [
    "create_secure_app",
    "setup_security_middleware", 
    "SecurityConfig",
    "verify_security_configuration",
    "initialize_security_components",
    "cleanup_security_components"
]