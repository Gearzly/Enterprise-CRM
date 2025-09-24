"""
Comprehensive input sanitization and validation utilities for enhanced security.
Provides sanitization for HTML, SQL injection prevention, XSS prevention,
and general input validation patterns.
"""
import re
import html
import urllib.parse
from typing import Any, Dict, List, Optional, Union
from enum import Enum

import bleach
import validators
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException, status


class SanitizationType(Enum):
    """Types of sanitization to apply"""
    HTML = "html"
    TEXT = "text"
    EMAIL = "email"
    URL = "url"
    PHONE = "phone"
    ALPHA_NUMERIC = "alphanumeric"
    NUMERIC = "numeric"
    SQL_SAFE = "sql_safe"


class InputSanitizer:
    """Main class for input sanitization and validation"""
    
    # Allowed HTML tags for rich text content
    ALLOWED_HTML_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 
        'h4', 'h5', 'h6', 'blockquote', 'a', 'img', 'span', 'div'
    ]
    
    # Allowed HTML attributes
    ALLOWED_HTML_ATTRIBUTES = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'span': ['class'],
        'div': ['class']
    }
    
    # Common SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\s*(union|select|insert|update|delete|drop|create|alter|exec|execute)\s+)",
        r"(\s*(or|and)\s+\d+\s*=\s*\d+)",
        r"(\s*--\s*)",
        r"(\s*/\*.*\*/\s*)",
        r"(\s*;\s*)",
        r"(\s*'\s*(or|and)\s*'.*')",
        r"(\s*\"\s*(or|and)\s*\".*\")"
    ]
    
    # XSS prevention patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"onclick\s*=",
        r"onmouseover\s*="
    ]
    
    @classmethod
    def sanitize_text(cls, text: str, max_length: Optional[int] = None) -> str:
        """Sanitize plain text input"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # HTML escape
        text = html.escape(text)
        
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    @classmethod
    def sanitize_html(cls, html_content: str, max_length: Optional[int] = None) -> str:
        """Sanitize HTML content allowing only safe tags"""
        if not isinstance(html_content, str):
            raise ValueError("Input must be a string")
        
        # Use bleach to sanitize HTML
        sanitized = bleach.clean(
            html_content,
            tags=cls.ALLOWED_HTML_TAGS,
            attributes=cls.ALLOWED_HTML_ATTRIBUTES,
            strip=True
        )
        
        # Additional XSS prevention
        for pattern in cls.XSS_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Limit length if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    @classmethod
    def validate_email(cls, email: str) -> str:
        """Validate and sanitize email address"""
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        email = email.strip().lower()
        
        try:
            # Use email-validator for comprehensive validation
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {str(e)}")
    
    @classmethod
    def validate_url(cls, url: str) -> str:
        """Validate and sanitize URL"""
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
        
        url = url.strip()
        
        # Check if URL is valid
        if not validators.url(url):
            raise ValueError("Invalid URL format")
        
        # Ensure HTTPS for external URLs
        if url.startswith('http://') and not url.startswith('http://localhost'):
            url = url.replace('http://', 'https://', 1)
        
        return url
    
    @classmethod
    def sanitize_phone(cls, phone: str) -> str:
        """Sanitize phone number"""
        if not isinstance(phone, str):
            raise ValueError("Phone must be a string")
        
        # Remove all non-digit characters except + and spaces
        phone = re.sub(r'[^\d\+\s\-\(\)]', '', phone)
        
        # Basic phone number validation
        digits_only = re.sub(r'[^\d]', '', phone)
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError("Invalid phone number length")
        
        return phone.strip()
    
    @classmethod
    def sanitize_alphanumeric(cls, text: str, allow_spaces: bool = True) -> str:
        """Sanitize to allow only alphanumeric characters"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        if allow_spaces:
            pattern = r'[^\w\s]'
        else:
            pattern = r'[^\w]'
        
        sanitized = re.sub(pattern, '', text)
        return sanitized.strip()
    
    @classmethod
    def sanitize_numeric(cls, value: str, allow_decimal: bool = True) -> str:
        """Sanitize to allow only numeric characters"""
        if not isinstance(value, str):
            raise ValueError("Input must be a string")
        
        if allow_decimal:
            pattern = r'[^\d\.]'
        else:
            pattern = r'[^\d]'
        
        sanitized = re.sub(pattern, '', value)
        
        # Validate numeric format
        try:
            if allow_decimal:
                float(sanitized) if sanitized else 0
            else:
                int(sanitized) if sanitized else 0
        except ValueError:
            raise ValueError("Invalid numeric format")
        
        return sanitized
    
    @classmethod
    def detect_sql_injection(cls, text: str) -> bool:
        """Detect potential SQL injection attempts"""
        if not isinstance(text, str):
            return False
        
        text_lower = text.lower()
        
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def sanitize_sql_safe(cls, text: str) -> str:
        """Sanitize text to prevent SQL injection"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        if cls.detect_sql_injection(text):
            raise ValueError("Potential SQL injection detected")
        
        # Escape single quotes
        text = text.replace("'", "''")
        
        # Remove dangerous SQL keywords in certain contexts
        dangerous_patterns = [
            r'\b(exec|execute|sp_|xp_)\b',
            r'\b(drop|create|alter)\s+\b',
            r'\b(union\s+select)\b'
        ]
        
        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @classmethod
    def sanitize_input(cls, value: Any, sanitization_type: SanitizationType, 
                      max_length: Optional[int] = None, **kwargs) -> Any:
        """Main sanitization method that routes to specific sanitizers"""
        if value is None:
            return None
        
        if not isinstance(value, str):
            value = str(value)
        
        if sanitization_type == SanitizationType.HTML:
            return cls.sanitize_html(value, max_length)
        elif sanitization_type == SanitizationType.TEXT:
            return cls.sanitize_text(value, max_length)
        elif sanitization_type == SanitizationType.EMAIL:
            return cls.validate_email(value)
        elif sanitization_type == SanitizationType.URL:
            return cls.validate_url(value)
        elif sanitization_type == SanitizationType.PHONE:
            return cls.sanitize_phone(value)
        elif sanitization_type == SanitizationType.ALPHA_NUMERIC:
            return cls.sanitize_alphanumeric(value, kwargs.get('allow_spaces', True))
        elif sanitization_type == SanitizationType.NUMERIC:
            return cls.sanitize_numeric(value, kwargs.get('allow_decimal', True))
        elif sanitization_type == SanitizationType.SQL_SAFE:
            return cls.sanitize_sql_safe(value)
        else:
            return cls.sanitize_text(value, max_length)


class SanitizedStr(str):
    """A string type that has been sanitized"""
    
    def __new__(cls, value: str, sanitization_type: SanitizationType = SanitizationType.TEXT, **kwargs):
        sanitized_value = InputSanitizer.sanitize_input(value, sanitization_type, **kwargs)
        return str.__new__(cls, sanitized_value)


# Pydantic validators for common sanitization needs
def sanitize_text_field(max_length: Optional[int] = None):
    """Pydantic validator for text fields"""
    def validator_func(cls, v):
        if v is None:
            return v
        return InputSanitizer.sanitize_text(v, max_length)
    return validator_func


def sanitize_html_field(max_length: Optional[int] = None):
    """Pydantic validator for HTML fields"""
    def validator_func(cls, v):
        if v is None:
            return v
        return InputSanitizer.sanitize_html(v, max_length)
    return validator_func


def sanitize_email_field():
    """Pydantic validator for email fields"""
    def validator_func(cls, v):
        if v is None:
            return v
        return InputSanitizer.validate_email(v)
    return validator_func


def sanitize_url_field():
    """Pydantic validator for URL fields"""
    def validator_func(cls, v):
        if v is None:
            return v
        return InputSanitizer.validate_url(v)
    return validator_func


# Middleware function for request sanitization
def sanitize_request_data(data: Dict[str, Any], 
                         field_types: Dict[str, SanitizationType]) -> Dict[str, Any]:
    """Sanitize request data based on field type specifications"""
    sanitized_data = {}
    
    for field_name, value in data.items():
        if field_name in field_types:
            try:
                sanitized_data[field_name] = InputSanitizer.sanitize_input(
                    value, field_types[field_name]
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid {field_name}: {str(e)}"
                )
        else:
            # Default to text sanitization
            sanitized_data[field_name] = InputSanitizer.sanitize_text(str(value))
    
    return sanitized_data


# Example sanitized models
class SanitizedUserInput(BaseModel):
    """Example model with built-in sanitization"""
    name: str = Field(..., max_length=100)
    email: str
    bio: Optional[str] = Field(None, max_length=1000)
    website: Optional[str] = None
    phone: Optional[str] = None
    
    # Validators
    _sanitize_name = validator('name', allow_reuse=True)(sanitize_text_field(100))
    _sanitize_email = validator('email', allow_reuse=True)(sanitize_email_field())
    _sanitize_bio = validator('bio', allow_reuse=True)(sanitize_html_field(1000))
    _sanitize_website = validator('website', allow_reuse=True)(sanitize_url_field())
    
    @validator('phone')
    def sanitize_phone(cls, v):
        if v is None:
            return v
        return InputSanitizer.sanitize_phone(v)


# Security headers for response
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}