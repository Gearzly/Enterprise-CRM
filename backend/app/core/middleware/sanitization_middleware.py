"""
Middleware for automatic input sanitization and security headers.
Automatically sanitizes incoming request data and adds security headers to responses.
"""
import json
import logging
from typing import Callable, Dict, Any, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException, status

from ..security.input_sanitization import (
    InputSanitizer, 
    SanitizationType, 
    SECURITY_HEADERS,
    sanitize_request_data
)

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for input sanitization and security headers"""
    
    def __init__(self, app, enable_sanitization: bool = True, enable_security_headers: bool = True):
        super().__init__(app)
        self.enable_sanitization = enable_sanitization
        self.enable_security_headers = enable_security_headers
        
        # Define sanitization rules for different endpoints
        self.sanitization_rules = {
            # Authentication endpoints
            "/api/superadmin/security/auth/token": {
                "username": SanitizationType.EMAIL,
                "password": SanitizationType.TEXT
            },
            "/api/superadmin/security/auth/register": {
                "email": SanitizationType.EMAIL,
                "password": SanitizationType.TEXT,
                "first_name": SanitizationType.ALPHA_NUMERIC,
                "last_name": SanitizationType.ALPHA_NUMERIC,
                "phone": SanitizationType.PHONE
            },
            
            # User management endpoints
            "/api/superadmin/users": {
                "email": SanitizationType.EMAIL,
                "first_name": SanitizationType.ALPHA_NUMERIC,
                "last_name": SanitizationType.ALPHA_NUMERIC,
                "phone": SanitizationType.PHONE,
                "bio": SanitizationType.HTML,
                "website": SanitizationType.URL
            },
            
            # Sales endpoints
            "/api/sales/leads": {
                "company_name": SanitizationType.TEXT,
                "contact_person": SanitizationType.TEXT,
                "email": SanitizationType.EMAIL,
                "phone": SanitizationType.PHONE,
                "website": SanitizationType.URL,
                "notes": SanitizationType.HTML,
                "source": SanitizationType.TEXT
            },
            "/api/sales/opportunities": {
                "title": SanitizationType.TEXT,
                "description": SanitizationType.HTML,
                "value": SanitizationType.NUMERIC,
                "probability": SanitizationType.NUMERIC
            },
            "/api/sales/accounts": {
                "name": SanitizationType.TEXT,
                "industry": SanitizationType.TEXT,
                "website": SanitizationType.URL,
                "phone": SanitizationType.PHONE,
                "email": SanitizationType.EMAIL,
                "description": SanitizationType.HTML
            },
            
            # Marketing endpoints
            "/api/marketing/campaigns": {
                "name": SanitizationType.TEXT,
                "description": SanitizationType.HTML,
                "subject": SanitizationType.TEXT,
                "content": SanitizationType.HTML,
                "target_audience": SanitizationType.TEXT
            },
            "/api/marketing/email": {
                "subject": SanitizationType.TEXT,
                "content": SanitizationType.HTML,
                "recipient_email": SanitizationType.EMAIL,
                "sender_name": SanitizationType.TEXT
            },
            
            # Support endpoints
            "/api/support/tickets": {
                "subject": SanitizationType.TEXT,
                "description": SanitizationType.HTML,
                "customer_email": SanitizationType.EMAIL,
                "customer_phone": SanitizationType.PHONE
            },
            "/api/support/knowledge-base": {
                "title": SanitizationType.TEXT,
                "content": SanitizationType.HTML,
                "category": SanitizationType.TEXT,
                "tags": SanitizationType.TEXT
            }
        }
        
        # Endpoints that should skip sanitization (file uploads, etc.)
        self.skip_sanitization_paths = [
            "/api/files/upload",
            "/api/files/download",
            "/docs",
            "/openapi.json",
            "/favicon.ico"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and response"""
        
        # Skip sanitization for certain paths
        if any(request.url.path.startswith(path) for path in self.skip_sanitization_paths):
            response = await call_next(request)
            return self._add_security_headers(response)
        
        # Only sanitize for POST, PUT, PATCH requests with JSON content
        if (self.enable_sanitization and 
            request.method in ["POST", "PUT", "PATCH"] and 
            request.headers.get("content-type", "").startswith("application/json")):
            
            try:
                request = await self._sanitize_request(request)
            except HTTPException as e:
                logger.warning(f"Input sanitization failed for {request.url.path}: {e.detail}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error during sanitization: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request data"
                )
        
        # Process the request
        response = await call_next(request)
        
        # Add security headers
        if self.enable_security_headers:
            response = self._add_security_headers(response)
        
        return response
    
    async def _sanitize_request(self, request: Request) -> Request:
        """Sanitize request data"""
        try:
            # Read request body
            body = await request.body()
            if not body:
                return request
            
            # Parse JSON data
            try:
                data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid JSON format"
                )
            
            # Get sanitization rules for this endpoint
            sanitization_rules = self._get_sanitization_rules(request.url.path)
            
            # Sanitize the data
            if sanitization_rules:
                sanitized_data = self._sanitize_data(data, sanitization_rules)
            else:
                # Apply default text sanitization
                sanitized_data = self._apply_default_sanitization(data)
            
            # Create new request with sanitized data
            sanitized_body = json.dumps(sanitized_data).encode('utf-8')
            
            # Update request with sanitized body
            async def receive():
                return {"type": "http.request", "body": sanitized_body}
            
            request._receive = receive
            
            return request
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error sanitizing request: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request processing error"
            )
    
    def _get_sanitization_rules(self, path: str) -> Optional[Dict[str, SanitizationType]]:
        """Get sanitization rules for a specific path"""
        # Exact match first
        if path in self.sanitization_rules:
            return self.sanitization_rules[path]
        
        # Pattern matching for dynamic paths (e.g., /api/users/{id})
        for rule_path, rules in self.sanitization_rules.items():
            if self._path_matches(path, rule_path):
                return rules
        
        return None
    
    def _path_matches(self, actual_path: str, rule_path: str) -> bool:
        """Check if actual path matches rule path pattern"""
        # Simple pattern matching - could be enhanced with regex
        actual_parts = actual_path.strip('/').split('/')
        rule_parts = rule_path.strip('/').split('/')
        
        if len(actual_parts) != len(rule_parts):
            return False
        
        for actual, rule in zip(actual_parts, rule_parts):
            if rule.startswith('{') and rule.endswith('}'):
                # Dynamic path parameter - matches anything
                continue
            elif actual != rule:
                return False
        
        return True
    
    def _sanitize_data(self, data: Any, rules: Dict[str, SanitizationType]) -> Any:
        """Sanitize data based on rules"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key in rules:
                    try:
                        sanitized[key] = InputSanitizer.sanitize_input(value, rules[key])
                    except ValueError as e:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid {key}: {str(e)}"
                        )
                else:
                    # Apply default sanitization for unknown fields
                    if isinstance(value, str):
                        sanitized[key] = InputSanitizer.sanitize_text(value)
                    else:
                        sanitized[key] = value
            return sanitized
        
        elif isinstance(data, list):
            return [self._sanitize_data(item, rules) for item in data]
        
        else:
            # For non-dict/list data, apply text sanitization if it's a string
            if isinstance(data, str):
                return InputSanitizer.sanitize_text(data)
            return data
    
    def _apply_default_sanitization(self, data: Any) -> Any:
        """Apply default text sanitization to all string fields"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if isinstance(value, str):
                    # Check for potential SQL injection or XSS
                    if InputSanitizer.detect_sql_injection(value):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Security violation detected in field: {key}"
                        )
                    sanitized[key] = InputSanitizer.sanitize_text(value)
                elif isinstance(value, (dict, list)):
                    sanitized[key] = self._apply_default_sanitization(value)
                else:
                    sanitized[key] = value
            return sanitized
        
        elif isinstance(data, list):
            return [self._apply_default_sanitization(item) for item in data]
        
        elif isinstance(data, str):
            if InputSanitizer.detect_sql_injection(data):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Security violation detected"
                )
            return InputSanitizer.sanitize_text(data)
        
        return data
    
    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response"""
        if self.enable_security_headers:
            for header, value in SECURITY_HEADERS.items():
                response.headers[header] = value
        
        return response


class SQLInjectionDetectionMiddleware(BaseHTTPMiddleware):
    """Specialized middleware for SQL injection detection"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check for SQL injection attempts"""
        
        # Check query parameters
        for param_name, param_value in request.query_params.items():
            if InputSanitizer.detect_sql_injection(str(param_value)):
                logger.warning(f"SQL injection attempt detected in query param {param_name}: {param_value}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request parameters"
                )
        
        # Check path parameters for SQL injection
        path = str(request.url.path)
        if InputSanitizer.detect_sql_injection(path):
            logger.warning(f"SQL injection attempt detected in path: {path}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request path"
            )
        
        return await call_next(request)


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Basic rate limiting middleware for authentication endpoints"""
    
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 300):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts = {}  # In production, use Redis
        
        # Endpoints that need rate limiting
        self.rate_limited_paths = [
            "/api/superadmin/security/auth/token",
            "/api/superadmin/security/auth/register",
            "/api/superadmin/security/auth/refresh",
            "/api/superadmin/security/auth/mfa"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply rate limiting"""
        
        # Check if this path needs rate limiting
        if not any(request.url.path.startswith(path) for path in self.rate_limited_paths):
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Simple in-memory rate limiting (use Redis in production)
        import time
        current_time = int(time.time())
        window_start = current_time - self.window_seconds
        
        # Clean old entries
        self.request_counts = {
            ip: [(timestamp, path) for timestamp, path in requests 
                 if timestamp > window_start]
            for ip, requests in self.request_counts.items()
        }
        
        # Count requests for this IP
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        current_requests = len(self.request_counts[client_ip])
        
        if current_requests >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP {client_ip}: {current_requests} requests")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        # Add current request
        self.request_counts[client_ip].append((current_time, request.url.path))
        
        return await call_next(request)