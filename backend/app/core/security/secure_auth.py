"""
Secure Authentication Alternatives to JWT
Implements multiple authentication mechanisms with enhanced security
"""
import os
import secrets
import hashlib
import time
import hmac
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AuthMethod(Enum):
    """Supported authentication methods"""
    SECURE_TOKEN = "secure_token"          # Opaque tokens with server-side validation
    OAUTH2_PKCE = "oauth2_pkce"           # OAuth 2.0 with PKCE
    WEBAUTHN = "webauthn"                 # WebAuthn/FIDO2
    CERTIFICATE = "certificate"           # Client certificate authentication
    TOTP_MFA = "totp_mfa"                # Time-based OTP
    SESSION_BASED = "session_based"       # Traditional session cookies

@dataclass
class SecureToken:
    """Secure token structure"""
    token_id: str
    user_id: str
    expires_at: datetime
    scope: List[str]
    created_at: datetime
    last_used: Optional[datetime] = None
    revoked: bool = False

@dataclass
class AuthSession:
    """Authentication session"""
    session_id: str
    user_id: str
    auth_method: AuthMethod
    expires_at: datetime
    created_at: datetime
    ip_address: str
    user_agent: str
    mfa_verified: bool = False
    risk_score: float = 0.0

class SecureTokenManager:
    """
    Secure token manager - Alternative to JWT
    
    Advantages over JWT:
    1. Server-side validation (can be revoked instantly)
    2. Opaque tokens (no information leakage)
    3. Cryptographically secure generation
    4. Built-in expiration and rotation
    5. Audit trail capabilities
    """
    
    def __init__(self):
        self.tokens: Dict[str, SecureToken] = {}
        self.cipher = Fernet(self._get_token_key())
    
    def _get_token_key(self) -> bytes:
        """Get token encryption key"""
        key = os.environ.get('TOKEN_ENCRYPTION_KEY')
        if not key:
            # Generate a new key for development
            key = Fernet.generate_key().decode()
            os.environ['TOKEN_ENCRYPTION_KEY'] = key
        return key.encode()
    
    def generate_token(self, user_id: str, scope: List[str], 
                      expires_in_minutes: int = 15) -> str:
        """Generate a secure token"""
        # Generate cryptographically secure token ID
        token_id = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        
        # Create token metadata
        token = SecureToken(
            token_id=token_id,
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=expires_in_minutes),
            scope=scope,
            created_at=datetime.utcnow()
        )
        
        # Store token (in production, use database)
        self.tokens[token_id] = token
        
        # Create encrypted token for client
        token_data = {
            'id': token_id,
            'exp': int(token.expires_at.timestamp()),
            'iat': int(token.created_at.timestamp())
        }
        
        encrypted_token = self.cipher.encrypt(str(token_data).encode())
        return base64.urlsafe_b64encode(encrypted_token).decode()
    
    def validate_token(self, token_str: str) -> Optional[SecureToken]:
        """Validate and return token if valid"""
        try:
            # Decrypt token
            encrypted_token = base64.urlsafe_b64decode(token_str.encode())
            decrypted_data = self.cipher.decrypt(encrypted_token)
            token_data = eval(decrypted_data.decode())  # In production, use JSON
            
            token_id = token_data['id']
            
            # Get token from storage
            token = self.tokens.get(token_id)
            if not token:
                return None
            
            # Check if token is expired or revoked
            if token.revoked or datetime.utcnow() > token.expires_at:
                return None
            
            # Update last used time
            token.last_used = datetime.utcnow()
            
            return token
            
        except Exception:
            return None
    
    def revoke_token(self, token_str: str) -> bool:
        """Revoke a token"""
        token = self.validate_token(token_str)
        if token:
            token.revoked = True
            return True
        return False
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens"""
        now = datetime.utcnow()
        expired_tokens = [
            token_id for token_id, token in self.tokens.items()
            if token.expires_at < now
        ]
        for token_id in expired_tokens:
            del self.tokens[token_id]

class OAuth2PKCEManager:
    """
    OAuth 2.0 with PKCE (Proof Key for Code Exchange)
    More secure than standard OAuth 2.0
    """
    
    def __init__(self):
        self.code_challenges: Dict[str, Dict[str, Any]] = {}
    
    def generate_pkce_challenge(self) -> Dict[str, str]:
        """Generate PKCE code challenge"""
        # Generate code verifier
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip('=')
        
        # Generate code challenge
        digest = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode().rstrip('=')
        
        return {
            'code_verifier': code_verifier,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
    
    def verify_pkce_challenge(self, code_verifier: str, code_challenge: str) -> bool:
        """Verify PKCE code challenge"""
        digest = hashlib.sha256(code_verifier.encode()).digest()
        expected_challenge = base64.urlsafe_b64encode(digest).decode().rstrip('=')
        return hmac.compare_digest(expected_challenge, code_challenge)

class SessionManager:
    """
    Traditional session-based authentication
    More secure for web applications than JWT
    """
    
    def __init__(self):
        self.sessions: Dict[str, AuthSession] = {}
        self.cipher = Fernet(self._get_session_key())
    
    def _get_session_key(self) -> bytes:
        """Get session encryption key"""
        key = os.environ.get('SESSION_SECRET_KEY')
        if not key:
            key = Fernet.generate_key().decode()
            os.environ['SESSION_SECRET_KEY'] = key
        return key.encode()
    
    def create_session(self, user_id: str, auth_method: AuthMethod,
                      ip_address: str, user_agent: str) -> str:
        """Create a new session"""
        session_id = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        
        session = AuthSession(
            session_id=session_id,
            user_id=user_id,
            auth_method=auth_method,
            expires_at=datetime.utcnow() + timedelta(hours=8),
            created_at=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        
        # Return encrypted session cookie
        session_data = {
            'id': session_id,
            'exp': int(session.expires_at.timestamp())
        }
        encrypted_session = self.cipher.encrypt(str(session_data).encode())
        return base64.urlsafe_b64encode(encrypted_session).decode()
    
    def validate_session(self, session_token: str, ip_address: str) -> Optional[AuthSession]:
        """Validate session"""
        try:
            # Decrypt session token
            encrypted_session = base64.urlsafe_b64decode(session_token.encode())
            decrypted_data = self.cipher.decrypt(encrypted_session)
            session_data = eval(decrypted_data.decode())
            
            session_id = session_data['id']
            session = self.sessions.get(session_id)
            
            if not session:
                return None
            
            # Check expiration
            if datetime.utcnow() > session.expires_at:
                del self.sessions[session_id]
                return None
            
            # Check IP address (optional security measure)
            # In production, you might want to be more flexible
            if session.ip_address != ip_address:
                # Log suspicious activity
                pass
            
            return session
            
        except Exception:
            return None

class WebAuthnManager:
    """
    WebAuthn/FIDO2 Authentication Manager
    Most secure authentication method available
    """
    
    def __init__(self):
        self.credentials: Dict[str, Dict[str, Any]] = {}
    
    def register_credential(self, user_id: str, credential_id: str, 
                          public_key: str, device_name: str) -> bool:
        """Register a WebAuthn credential"""
        self.credentials[credential_id] = {
            'user_id': user_id,
            'public_key': public_key,
            'device_name': device_name,
            'created_at': datetime.utcnow(),
            'sign_count': 0
        }
        return True
    
    def authenticate_credential(self, credential_id: str, 
                              signature: str, challenge: str) -> Optional[str]:
        """Authenticate using WebAuthn credential"""
        credential = self.credentials.get(credential_id)
        if not credential:
            return None
        
        # In a real implementation, verify the signature
        # This is a simplified version
        if self._verify_signature(credential['public_key'], signature, challenge):
            credential['sign_count'] += 1
            return credential['user_id']
        
        return None
    
    def _verify_signature(self, public_key: str, signature: str, challenge: str) -> bool:
        """Verify WebAuthn signature (simplified)"""
        # In production, use a proper WebAuthn library
        return True  # Placeholder

def create_security_recommendations():
    """Generate security recommendations for authentication"""
    return {
        "immediate_actions": [
            "Replace JWT with secure token system",
            "Implement WebAuthn for passwordless authentication",
            "Enable MFA for all user accounts",
            "Use HTTPS-only cookies with SameSite=Strict",
            "Implement session timeout and rotation"
        ],
        "authentication_hierarchy": [
            "1. WebAuthn/FIDO2 (Most Secure)",
            "2. OAuth 2.0 with PKCE + MFA",
            "3. Secure Session-based authentication",
            "4. Secure Token system (JWT alternative)",
            "5. Traditional JWT (Least Secure - Avoid)"
        ],
        "jwt_vulnerabilities": [
            "Algorithm confusion attacks",
            "Key confusion attacks",
            "Token sidejacking",
            "Weak secret keys",
            "No revocation capability",
            "Information disclosure in payload",
            "Timing attacks on verification"
        ]
    }

# Initialize managers
secure_token_manager = SecureTokenManager()
oauth2_pkce_manager = OAuth2PKCEManager()
session_manager = SessionManager()
webauthn_manager = WebAuthnManager()

# Export security recommendations
SECURITY_RECOMMENDATIONS = create_security_recommendations()