"""
OWASP Security Implementation Module

This module implements comprehensive OWASP security measures:
- Input validation and sanitization
- Rate limiting
- Security headers
- Content Security Policy
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Optional, Callable, Awaitable
from datetime import datetime, timedelta
import re
import html
import json
import logging
from collections import defaultdict
from functools import wraps

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Rate limiting storage (in production, use Redis or similar)
rate_limit_storage: Dict[str, Dict[str, datetime]] = defaultdict(dict)
rate_limit_counts: Dict[str, Dict[str, int]] = defaultdict(dict)

class OWASPSecurityMiddleware:
    """Middleware for implementing OWASP security measures"""
    
    def __init__(self, app: FastAPI):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Add security headers to all responses
        async def add_security_headers(message):
            if message["type"] == "http.response.start":
                # Add security headers
                headers = message.get("headers", [])
                headers.extend([
                    (b"X-Content-Type-Options", b"nosniff"),
                    (b"X-Frame-Options", b"DENY"),
                    (b"X-XSS-Protection", b"1; mode=block"),
                    (b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains"),
                    (b"Content-Security-Policy", b"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"),
                    (b"Referrer-Policy", b"strict-origin-when-cross-origin"),
                ])
                message["headers"] = headers
            await send(message)
        
        await self.app(scope, receive, add_security_headers)

def add_security_headers(app: FastAPI):
    """Add OWASP security headers to the FastAPI app"""
    app.add_middleware(OWASPSecurityMiddleware)

def sanitize_input(value: str) -> str:
    """Sanitize user input to prevent XSS and other injection attacks"""
    if not isinstance(value, str):
        return str(value)
    
    # HTML escape to prevent XSS
    sanitized = html.escape(value)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', sanitized)
    
    # Limit length to prevent overflow attacks
    return sanitized[:1000]  # Limit to 1000 characters

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^\+?[\d\s\-\(\)]{7,15}$'
    return re.match(pattern, phone) is not None

def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from args (assuming it's the first argument)
            request = None
            for arg in args:
                if hasattr(arg, 'client'):
                    request = arg
                    break
            
            if request:
                # Get client IP
                client_ip = request.client.host if request.client else "unknown"
                
                # Get current time
                now = datetime.utcnow()
                window_key = f"{func.__name__}_{client_ip}"
                
                # Clean up old entries
                if window_key in rate_limit_storage:
                    expired_keys = [
                        key for key, timestamp in rate_limit_storage[window_key].items()
                        if now - timestamp > timedelta(seconds=window_seconds)
                    ]
                    for key in expired_keys:
                        del rate_limit_storage[window_key][key]
                        if window_key in rate_limit_counts and key in rate_limit_counts[window_key]:
                            del rate_limit_counts[window_key][key]
                
                # Count requests
                current_count = rate_limit_counts[window_key].get(str(now), 0)
                if current_count >= max_requests:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                
                # Update count
                rate_limit_counts[window_key][str(now)] = current_count + 1
                rate_limit_storage[window_key][str(now)] = now
            
            # Call the original function
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def validate_json_payload(payload: str) -> dict:
    """Validate and sanitize JSON payload"""
    try:
        # Parse JSON
        data = json.loads(payload)
        
        # Recursively sanitize all string values
        def sanitize_dict(d):
            if isinstance(d, dict):
                return {k: sanitize_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [sanitize_dict(item) for item in d]
            elif isinstance(d, str):
                return sanitize_input(d)
            else:
                return d
        
        return sanitize_dict(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

def apply_content_security_policy(response: JSONResponse) -> JSONResponse:
    """Apply Content Security Policy to response"""
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "media-src 'self'; "
        "frame-src 'none'; "
        "object-src 'none'"
    )
    return response

# Input validation functions for common data types
def validate_input_string(value: str, max_length: int = 255, allow_empty: bool = False) -> str:
    """Validate and sanitize a string input"""
    if not isinstance(value, str):
        raise HTTPException(status_code=400, detail="Invalid input type")
    
    if not allow_empty and not value.strip():
        raise HTTPException(status_code=400, detail="Input cannot be empty")
    
    if len(value) > max_length:
        raise HTTPException(status_code=400, detail=f"Input exceeds maximum length of {max_length}")
    
    return sanitize_input(value)

def validate_input_integer(value: str, min_value: int = 0, max_value: int = 2147483647) -> int:
    """Validate and convert string to integer"""
    try:
        int_value = int(value)
        if int_value < min_value or int_value > max_value:
            raise HTTPException(status_code=400, detail=f"Integer value must be between {min_value} and {max_value}")
        return int_value
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integer value")

def validate_input_boolean(value: str) -> bool:
    """Validate and convert string to boolean"""
    if value.lower() in ['true', '1', 'yes', 'on']:
        return True
    elif value.lower() in ['false', '0', 'no', 'off']:
        return False
    else:
        raise HTTPException(status_code=400, detail="Invalid boolean value")

# Security middleware for request validation
async def security_middleware(request: Request, call_next):
    """Middleware to apply security checks to all requests"""
    
    # Log the request
    logger.info(f"Security check for {request.method} {request.url}")
    
    # Apply rate limiting
    client_ip = request.client.host if request.client else "unknown"
    endpoint = f"{request.method}_{request.url.path}"
    
    # Check rate limit
    now = datetime.utcnow()
    window_key = f"{endpoint}_{client_ip}"
    
    # Clean up old entries
    if window_key in rate_limit_storage:
        expired_keys = [
            key for key, timestamp in rate_limit_storage[window_key].items()
            if now - timestamp > timedelta(hours=1)  # 1 hour window
        ]
        for key in expired_keys:
            del rate_limit_storage[window_key][key]
            if window_key in rate_limit_counts and key in rate_limit_counts[window_key]:
                del rate_limit_counts[window_key][key]
    
    # Count requests in current window
    current_window_requests = sum(
        1 for timestamp in rate_limit_storage[window_key].values()
        if now - timestamp < timedelta(hours=1)
    )
    
    if current_window_requests > 1000:  # Max 1000 requests per hour per IP
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    
    # Record this request
    rate_limit_storage[window_key][str(now)] = now
    if window_key not in rate_limit_counts:
        rate_limit_counts[window_key] = defaultdict(int)
    rate_limit_counts[window_key][str(now)] += 1
    
    # Process the request
    response = await call_next(request)
    
    # Apply security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Apply Content Security Policy
    apply_content_security_policy(response)
    
    return response

# SQL Injection prevention functions
def sanitize_sql_input(value: str) -> str:
    """Basic SQL injection prevention (in addition to using parameterized queries)"""
    # Remove common SQL injection patterns
    patterns = [
        r"(\b)(union|select|insert|update|delete|drop|create|alter|exec|execute)(\b)",
        r"([';])\s*(union|select|insert|update|delete|drop|create|alter|exec|execute)",
        r"--",
        r"/\*.*?\*/",
        r"xp_",
        r"sp_"
    ]
    
    sanitized = value
    for pattern in patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()

# Cross-Site Request Forgery (CSRF) protection
csrf_tokens: Dict[str, Dict[str, datetime]] = {}

def generate_csrf_token(user_id: str) -> str:
    """Generate a CSRF token for a user"""
    import secrets
    token = secrets.token_urlsafe(32)
    csrf_tokens[user_id] = {
        "token": token,
        "created_at": datetime.utcnow()
    }
    return token

def validate_csrf_token(user_id: str, token: str) -> bool:
    """Validate a CSRF token"""
    if user_id not in csrf_tokens:
        return False
    
    token_data = csrf_tokens[user_id]
    
    # Check if token is expired (1 hour validity)
    if datetime.utcnow() - token_data["created_at"] > timedelta(hours=1):
        del csrf_tokens[user_id]
        return False
    
    # Check if token matches
    is_valid = token_data["token"] == token
    
    # Remove used token
    if is_valid:
        del csrf_tokens[user_id]
    
    return is_valid