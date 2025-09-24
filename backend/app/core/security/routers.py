"""
API Routers for Security Features

This module provides FastAPI endpoints for security operations.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .owasp import (
    sanitize_input,
    validate_email,
    validate_phone,
    rate_limit,
    validate_json_payload,
    validate_input_string,
    validate_input_integer,
    validate_input_boolean
)

# Create routers
security_router = APIRouter(prefix="/security", tags=["Security"])

class SanitizeRequest(BaseModel):
    """Request model for input sanitization"""
    input_text: str

class SanitizeResponse(BaseModel):
    """Response model for input sanitization"""
    original_text: str
    sanitized_text: str

class ValidateEmailRequest(BaseModel):
    """Request model for email validation"""
    email: str

class ValidateEmailResponse(BaseModel):
    """Response model for email validation"""
    email: str
    is_valid: bool

class ValidatePhoneRequest(BaseModel):
    """Request model for phone validation"""
    phone: str

class ValidatePhoneResponse(BaseModel):
    """Response model for phone validation"""
    phone: str
    is_valid: bool

class ValidateJsonRequest(BaseModel):
    """Request model for JSON validation"""
    json_payload: str

class ValidateJsonResponse(BaseModel):
    """Response model for JSON validation"""
    is_valid: bool
    sanitized_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Input Sanitization Endpoints
@security_router.post("/sanitize", response_model=SanitizeResponse)
async def sanitize_input_endpoint(request: SanitizeRequest):
    """Sanitize user input to prevent XSS and injection attacks"""
    sanitized = sanitize_input(request.input_text)
    return SanitizeResponse(
        original_text=request.input_text,
        sanitized_text=sanitized
    )

@security_router.post("/validate/email", response_model=ValidateEmailResponse)
async def validate_email_endpoint(request: ValidateEmailRequest):
    """Validate email format"""
    is_valid = validate_email(request.email)
    return ValidateEmailResponse(
        email=request.email,
        is_valid=is_valid
    )

@security_router.post("/validate/phone", response_model=ValidatePhoneResponse)
async def validate_phone_endpoint(request: ValidatePhoneRequest):
    """Validate phone number format"""
    is_valid = validate_phone(request.phone)
    return ValidatePhoneResponse(
        phone=request.phone,
        is_valid=is_valid
    )

@security_router.post("/validate/json", response_model=ValidateJsonResponse)
async def validate_json_endpoint(request: ValidateJsonRequest):
    """Validate and sanitize JSON payload"""
    try:
        sanitized_data = validate_json_payload(request.json_payload)
        return ValidateJsonResponse(
            is_valid=True,
            sanitized_data=sanitized_data
        )
    except Exception as e:
        return ValidateJsonResponse(
            is_valid=False,
            error=str(e)
        )

# Rate Limiting Test Endpoint
@security_router.get("/test/rate-limit")
@rate_limit(max_requests=5, window_seconds=60)  # 5 requests per minute
async def rate_limit_test():
    """Test endpoint for rate limiting"""
    return {"message": "This endpoint is rate limited to 5 requests per minute"}

# Input Validation Endpoints
@security_router.post("/validate/string")
async def validate_string(input_text: str, max_length: int = 255, allow_empty: bool = False):
    """Validate and sanitize a string input"""
    try:
        validated = validate_input_string(input_text, max_length, allow_empty)
        return {"validated_text": validated}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@security_router.post("/validate/integer")
async def validate_integer(input_text: str, min_value: int = 0, max_value: int = 2147483647):
    """Validate and convert string to integer"""
    try:
        validated = validate_input_integer(input_text, min_value, max_value)
        return {"validated_integer": validated}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@security_router.post("/validate/boolean")
async def validate_boolean(input_text: str):
    """Validate and convert string to boolean"""
    try:
        validated = validate_input_boolean(input_text)
        return {"validated_boolean": validated}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Security Configuration Endpoint
@security_router.get("/config")
async def get_security_config():
    """Get current security configuration"""
    return {
        "rate_limiting": {
            "enabled": True,
            "default_limit": "1000 requests/hour",
            "endpoint_limits": {
                "/api/security/test/rate-limit": "5 requests/minute"
            }
        },
        "input_validation": {
            "enabled": True,
            "sanitization": "HTML escaping and character filtering",
            "max_length": 1000
        },
        "headers": {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    }