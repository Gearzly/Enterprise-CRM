# PROJECT DEVELOPMENT RULES AND GUIDELINES
# CRM Backend OAuth2+PKCE Migration Project

## Security Standards (MANDATORY)

### 1. Authentication System
- **MUST** use OAuth2 with PKCE (RFC 6749 + RFC 7636) for all authentication
- **MUST NOT** implement new JWT-based authentication systems
- **MUST** use PKCE challenge method S256 only
- **MUST** implement proper code verifier generation (32+ bytes, URL-safe base64)

### 2. Token Management
- **MUST** use opaque tokens (not self-contained like JWT)
- **MUST** implement token rotation for refresh tokens
- **MUST** provide immediate token revocation capability
- **MUST** set appropriate token expiration times:
  - Access tokens: 15-60 minutes maximum
  - Refresh tokens: 1-30 days maximum
  - Authorization codes: 10 minutes maximum

### 3. Input Validation
- **MUST** use parameterized queries for all database operations
- **MUST** validate all user inputs against expected patterns
- **MUST** sanitize all HTML inputs using bleach library
- **MUST** implement Content Security Policy (CSP) headers

### 4. OWASP Security Headers (MANDATORY)
```python
REQUIRED_SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}
```

## Code Quality Standards

### 1. Python Standards
- **MUST** use type hints for all functions and class attributes
- **MUST** follow PEP 8 style guidelines
- **MUST** use descriptive function and variable names
- **MUST** keep functions under 50 lines when possible

### 2. Documentation Requirements
```python
def generate_pkce_challenge() -> Dict[str, str]:
    """
    Generate PKCE challenge for OAuth 2.0 flow.
    
    Implements RFC 7636 Section 4.1 for generating code_challenge
    from a cryptographically secure code_verifier.
    
    Returns:
        Dict containing code_challenge, code_challenge_method, challenge_id
        
    Raises:
        CryptographicError: If secure random generation fails
    """
```

### 3. Error Handling
```python
# MUST use specific exception types
class AuthenticationError(HTTPException):
    """Authentication failed."""
    pass

# MUST include proper error context
try:
    result = oauth2_manager.validate_token(token)
except TokenExpiredError as e:
    logger.warning(f"Token expired for user {user_id}: {e}")
    raise AuthenticationError("Token expired")
```

## Testing Requirements

### 1. Coverage Standards
- **Unit Tests**: 90% code coverage minimum
- **Integration Tests**: All API endpoints must be tested
- **Security Tests**: All authentication/authorization paths
- **Performance Tests**: All critical endpoints under load

### 2. Test Structure
```python
class TestOAuth2PKCEManager:
    """Test OAuth2 PKCE manager functionality."""
    
    def test_generate_pkce_challenge_success(self):
        """Test successful PKCE challenge generation."""
        pass
        
    def test_generate_pkce_challenge_crypto_failure(self):
        """Test PKCE challenge generation with crypto failure."""
        pass
```

## API Development Guidelines

### 1. URL Structure
```python
# Resource-based URLs
GET    /api/v1/users                 # List users
POST   /api/v1/users                 # Create user
PUT    /api/v1/users/{user_id}       # Update user

# OAuth2 endpoints
POST   /auth/challenge               # Generate PKCE challenge
POST   /auth/token                   # Token exchange
POST   /auth/refresh                 # Refresh token
```

### 2. Response Format
```python
# MUST use consistent response format
{
    "success": true,
    "data": {"user_id": "123", "email": "user@example.com"},
    "message": "User retrieved successfully",
    "metadata": {"request_id": "req_123", "timestamp": "2025-01-01T00:00:00Z"}
}
```

### 3. Rate Limiting (MANDATORY)
```python
RATE_LIMITS = {
    '/auth/token': '5/minute',           # Authentication attempts
    '/auth/challenge': '10/minute',      # PKCE challenges
    '/api/v1/users': '100/hour',         # General API usage
    'default': '1000/hour'               # Default limit
}
```

## Database and Security

### 1. Database Security
- **MUST** use connection pooling
- **MUST** encrypt PII data at rest
- **MUST** use field-level encryption for sensitive data
- **MUST** implement audit trails for data access

### 2. Data Classification
```python
class DataClassification(Enum):
    PUBLIC = "public"           # Can be freely shared
    INTERNAL = "internal"       # Internal use only
    CONFIDENTIAL = "confidential"  # Restricted access
    RESTRICTED = "restricted"   # Highest protection level
```

## Logging and Monitoring

### 1. Logging Requirements
```python
# MUST use appropriate log levels
logger.error("OAuth2 token validation failed", extra={
    'user_id': user_id,
    'token_id': token_id,
    'error': str(e)
})

logger.warning("Multiple failed login attempts", extra={
    'email': email,
    'ip_address': request.client.host,
    'attempt_count': attempt_count
})
```

### 2. Performance Standards
```python
RESPONSE_TIME_TARGETS = {
    'authentication_endpoints': 500,    # milliseconds
    'read_operations': 200,             # milliseconds
    'write_operations': 1000,           # milliseconds
    'complex_queries': 2000             # milliseconds
}
```

## Deployment Standards

### 1. Environment Variables (MANDATORY)
```python
# Security Configuration
OAUTH2_ENCRYPTION_KEY=<fernet-key>      # Token encryption
SECRET_ENCRYPTION_KEY=<fernet-key>      # Session encryption
DATABASE_URL=<connection-string>        # Database connection

# OAuth2 Configuration  
OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES=60
OAUTH2_REFRESH_TOKEN_EXPIRE_DAYS=30

# Security Features
ENABLE_MFA=true
RATE_LIMIT_ENABLED=true
AUDIT_LOG_ENABLED=true
```

### 2. Container Security
- **MUST** run as non-root user
- **MUST** use HTTPS in production
- **MUST** implement health checks
- **MUST** disable debug mode in production

## Compliance Requirements

### 1. Security Activities
- **MUST** perform monthly security reviews
- **MUST** patch critical vulnerabilities within 48 hours
- **MUST** rotate encryption keys quarterly
- **MUST** scan for vulnerabilities weekly

### 2. Code Review Process
- **MUST** require code review for all changes
- **MUST** require security review for authentication changes
- **MUST** include security checklist in reviews
- **MUST** test rollback procedures quarterly

## Development Tools (MANDATORY)

### 1. Required Tools
```bash
pytest>=7.0.0           # Testing framework
pytest-cov>=4.0.0       # Coverage reporting
black>=22.0.0           # Code formatting
mypy>=1.0.0             # Type checking
bandit>=1.7.0           # Security linting
```

### 2. Pre-commit Hooks
```yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/bandit
    hooks:
      - id: bandit
```

## Issue Resolution Guidelines

### 1. Current Critical Issues
1. **Server Startup Syntax Error** (Priority 1)
   - Location: `app/superadmin/security/auth.py`
   - Issue: Unterminated triple-quoted string literal
   - Action: Fix docstring formatting

2. **OAuth2 Endpoint Testing** (Priority 2)
   - Issue: Cannot validate OAuth2 flow due to server startup
   - Action: Complete server startup, then run comprehensive tests

### 2. Migration Validation Checklist
- [ ] Server starts without syntax errors
- [ ] OAuth2 challenge endpoint accessible
- [ ] Token exchange flow working
- [ ] JWT endpoints properly deprecated
- [ ] Security headers implemented
- [ ] All tests passing with 90%+ coverage

---

**Document Version**: 1.0  
**Last Updated**: 2025-09-24  
**Compliance**: OAuth2+PKCE Migration Project Standards