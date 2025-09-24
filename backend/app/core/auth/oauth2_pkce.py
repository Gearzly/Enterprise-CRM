"""
OAuth 2.0 with PKCE (Proof Key for Code Exchange) Authentication System
Replaces JWT with a more secure authentication mechanism

OAuth 2.0 with PKCE provides:
1. Authorization code flow with PKCE (RFC 7636)
2. No sensitive data in tokens
3. Automatic token rotation
4. Immediate revocation capability
5. Protection against authorization code interception
6. Client authentication without client secrets
"""
import os
import secrets
import hashlib
import base64
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass, field
from urllib.parse import urlencode, parse_qs
from fastapi import HTTPException, status
from pydantic import BaseModel
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class GrantType(Enum):
    """OAuth 2.0 Grant Types"""
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"
    CLIENT_CREDENTIALS = "client_credentials"

class TokenType(Enum):
    """Token Types"""
    BEARER = "Bearer"
    MAC = "mac"

@dataclass
class PKCEChallenge:
    """PKCE Challenge data"""
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=10))

@dataclass
class AuthorizationCode:
    """Authorization Code data"""
    code: str
    client_id: str
    user_id: str
    scope: List[str]
    code_challenge: str
    code_challenge_method: str
    expires_at: datetime
    used: bool = False

@dataclass
class OAuth2Token:
    """OAuth 2.0 Token"""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

@dataclass
class AccessToken:
    """Access Token metadata"""
    token: str
    client_id: str
    user_id: str
    scope: List[str]
    expires_at: datetime
    created_at: datetime = field(default_factory=datetime.utcnow)
    revoked: bool = False

@dataclass
class RefreshToken:
    """Refresh Token metadata"""
    token: str
    access_token: str
    client_id: str
    user_id: str
    expires_at: datetime
    created_at: datetime = field(default_factory=datetime.utcnow)
    revoked: bool = False

@dataclass
class OAuth2Client:
    """OAuth 2.0 Client"""
    client_id: str
    client_name: str
    redirect_uris: List[str]
    allowed_scopes: List[str]
    is_confidential: bool = False
    client_secret: Optional[str] = None

class OAuth2PKCEManager:
    """
    OAuth 2.0 with PKCE Manager
    
    Implements RFC 6749 (OAuth 2.0) with RFC 7636 (PKCE)
    """
    
    def __init__(self):
        self.pkce_challenges: Dict[str, PKCEChallenge] = {}
        self.authorization_codes: Dict[str, AuthorizationCode] = {}
        self.access_tokens: Dict[str, AccessToken] = {}
        self.refresh_tokens: Dict[str, RefreshToken] = {}
        self.clients: Dict[str, OAuth2Client] = {}
        self.cipher = Fernet(self._get_encryption_key())
        
        # Initialize default client for CRM
        self._initialize_default_client()
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key for token encryption"""
        key = os.environ.get('OAUTH2_ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key().decode()
            os.environ['OAUTH2_ENCRYPTION_KEY'] = key
            logger.warning("Generated new OAuth2 encryption key - store securely in production")
        return key.encode()
    
    def _initialize_default_client(self):
        """Initialize default CRM client"""
        default_client = OAuth2Client(
            client_id="crm_web_app",
            client_name="CRM Web Application",
            redirect_uris=["http://localhost:3000/auth/callback", "http://localhost:8000/auth/callback"],
            allowed_scopes=["read", "write", "admin", "sales", "marketing", "support"],
            is_confidential=False  # Public client (SPA/Mobile app)
        )
        self.clients[default_client.client_id] = default_client
    
    def generate_pkce_challenge(self) -> Dict[str, str]:
        """
        Generate PKCE challenge (RFC 7636)
        Returns code_challenge and code_verifier
        """
        # Generate code verifier (43-128 characters)
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        
        # Generate code challenge using S256 method
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        # Store challenge temporarily
        challenge_id = secrets.token_urlsafe(16)
        self.pkce_challenges[challenge_id] = PKCEChallenge(
            code_verifier=code_verifier,
            code_challenge=code_challenge
        )
        
        return {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "challenge_id": challenge_id,  # For internal tracking
            "state": secrets.token_urlsafe(16)  # CSRF protection
        }
    
    def generate_authorization_url(self, client_id: str, redirect_uri: str, 
                                 scope: List[str], code_challenge: str,
                                 state: str) -> str:
        """Generate OAuth 2.0 authorization URL"""
        if client_id not in self.clients:
            raise HTTPException(status_code=400, detail="Invalid client_id")
        
        client = self.clients[client_id]
        if redirect_uri not in client.redirect_uris:
            raise HTTPException(status_code=400, detail="Invalid redirect_uri")
        
        # Validate scope
        invalid_scopes = set(scope) - set(client.allowed_scopes)
        if invalid_scopes:
            raise HTTPException(status_code=400, detail=f"Invalid scopes: {invalid_scopes}")
        
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(scope),
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": state
        }
        
        base_url = os.environ.get("OAUTH2_AUTHORIZATION_URL", "http://localhost:8000/auth/authorize")
        return f"{base_url}?{urlencode(params)}"
    
    def create_authorization_code(self, client_id: str, user_id: str, 
                                scope: List[str], code_challenge: str,
                                code_challenge_method: str = "S256") -> str:
        """Create authorization code"""
        if client_id not in self.clients:
            raise HTTPException(status_code=400, detail="Invalid client_id")
        
        # Generate secure authorization code
        auth_code = secrets.token_urlsafe(32)
        
        # Store authorization code
        self.authorization_codes[auth_code] = AuthorizationCode(
            code=auth_code,
            client_id=client_id,
            user_id=user_id,
            scope=scope,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            expires_at=datetime.utcnow() + timedelta(minutes=10)  # Short-lived
        )
        
        return auth_code
    
    def exchange_code_for_token(self, code: str, client_id: str,
                              code_verifier: str, redirect_uri: str) -> OAuth2Token:
        """
        Exchange authorization code for access token
        Implements PKCE verification (RFC 7636 Section 4.6)
        """
        # Validate authorization code
        auth_code_data = self.authorization_codes.get(code)
        if not auth_code_data:
            raise HTTPException(status_code=400, detail="Invalid authorization code")
        
        if auth_code_data.used:
            raise HTTPException(status_code=400, detail="Authorization code already used")
        
        if datetime.utcnow() > auth_code_data.expires_at:
            raise HTTPException(status_code=400, detail="Authorization code expired")
        
        if auth_code_data.client_id != client_id:
            raise HTTPException(status_code=400, detail="Client ID mismatch")
        
        # Verify PKCE challenge
        if not self._verify_pkce_challenge(code_verifier, auth_code_data.code_challenge):
            raise HTTPException(status_code=400, detail="Invalid code verifier")
        
        # Mark code as used
        auth_code_data.used = True
        
        # Generate access token
        access_token = self._generate_access_token(
            client_id=client_id,
            user_id=auth_code_data.user_id,
            scope=auth_code_data.scope
        )
        
        # Generate refresh token
        refresh_token = self._generate_refresh_token(
            access_token=access_token,
            client_id=client_id,
            user_id=auth_code_data.user_id
        )
        
        return OAuth2Token(
            access_token=access_token,
            token_type=TokenType.BEARER.value,
            expires_in=3600,  # 1 hour
            refresh_token=refresh_token,
            scope=" ".join(auth_code_data.scope)
        )
    
    def _verify_pkce_challenge(self, code_verifier: str, code_challenge: str) -> bool:
        """Verify PKCE code challenge"""
        # Recreate challenge from verifier
        expected_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        # Constant-time comparison
        import hmac
        return hmac.compare_digest(expected_challenge, code_challenge)
    
    def _generate_access_token(self, client_id: str, user_id: str, scope: List[str]) -> str:
        """Generate encrypted access token"""
        # Create token payload
        token_data = {
            "client_id": client_id,
            "user_id": user_id,
            "scope": scope,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,  # 1 hour
            "jti": secrets.token_urlsafe(16)  # JWT ID for revocation
        }
        
        # Encrypt token payload
        encrypted_payload = self.cipher.encrypt(json.dumps(token_data).encode())
        access_token = base64.urlsafe_b64encode(encrypted_payload).decode()
        
        # Store token metadata
        self.access_tokens[access_token] = AccessToken(
            token=access_token,
            client_id=client_id,
            user_id=user_id,
            scope=scope,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        
        return access_token
    
    def _generate_refresh_token(self, access_token: str, client_id: str, user_id: str) -> str:
        """Generate refresh token"""
        refresh_token = secrets.token_urlsafe(32)
        
        self.refresh_tokens[refresh_token] = RefreshToken(
            token=refresh_token,
            access_token=access_token,
            client_id=client_id,
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(days=30)  # 30 days
        )
        
        return refresh_token
    
    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate and decode access token"""
        try:
            token_metadata = self.access_tokens.get(token)
            if not token_metadata:
                return None
            
            if token_metadata.revoked:
                return None
            
            if datetime.utcnow() > token_metadata.expires_at:
                return None
            
            # Decrypt token payload
            try:
                encrypted_payload = base64.urlsafe_b64decode(token.encode())
                decrypted_data = self.cipher.decrypt(encrypted_payload)
                token_data = json.loads(decrypted_data.decode())
                
                return {
                    "client_id": token_metadata.client_id,
                    "user_id": token_metadata.user_id,
                    "scope": token_metadata.scope,
                    "exp": int(token_metadata.expires_at.timestamp())
                }
            except Exception:
                return None
                
        except Exception:
            return None
    
    def refresh_access_token(self, refresh_token: str, client_id: str) -> OAuth2Token:
        """Refresh access token using refresh token"""
        refresh_data = self.refresh_tokens.get(refresh_token)
        if not refresh_data:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        
        if refresh_data.revoked:
            raise HTTPException(status_code=400, detail="Refresh token revoked")
        
        if datetime.utcnow() > refresh_data.expires_at:
            raise HTTPException(status_code=400, detail="Refresh token expired")
        
        if refresh_data.client_id != client_id:
            raise HTTPException(status_code=400, detail="Client ID mismatch")
        
        # Revoke old access token
        old_access_token = self.access_tokens.get(refresh_data.access_token)
        if old_access_token:
            old_access_token.revoked = True
        
        # Generate new access token
        new_access_token = self._generate_access_token(
            client_id=client_id,
            user_id=refresh_data.user_id,
            scope=[]  # Use stored scope from client
        )
        
        # Generate new refresh token
        new_refresh_token = self._generate_refresh_token(
            access_token=new_access_token,
            client_id=client_id,
            user_id=refresh_data.user_id
        )
        
        # Revoke old refresh token
        refresh_data.revoked = True
        
        return OAuth2Token(
            access_token=new_access_token,
            token_type=TokenType.BEARER.value,
            expires_in=3600,
            refresh_token=new_refresh_token
        )
    
    def revoke_token(self, token: str, token_type: str = "access_token") -> bool:
        """Revoke access or refresh token"""
        if token_type == "access_token":
            token_data = self.access_tokens.get(token)
            if token_data:
                token_data.revoked = True
                return True
        elif token_type == "refresh_token":
            token_data = self.refresh_tokens.get(token)
            if token_data:
                token_data.revoked = True
                # Also revoke associated access token
                access_token_data = self.access_tokens.get(token_data.access_token)
                if access_token_data:
                    access_token_data.revoked = True
                return True
        
        return False
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens and codes"""
        now = datetime.utcnow()
        
        # Clean up authorization codes
        expired_codes = [
            code for code, data in self.authorization_codes.items()
            if data.expires_at < now
        ]
        for code in expired_codes:
            del self.authorization_codes[code]
        
        # Clean up PKCE challenges
        expired_challenges = [
            challenge_id for challenge_id, data in self.pkce_challenges.items()
            if data.expires_at < now
        ]
        for challenge_id in expired_challenges:
            del self.pkce_challenges[challenge_id]
        
        # Clean up access tokens
        expired_access_tokens = [
            token for token, data in self.access_tokens.items()
            if data.expires_at < now
        ]
        for token in expired_access_tokens:
            del self.access_tokens[token]
        
        # Clean up refresh tokens
        expired_refresh_tokens = [
            token for token, data in self.refresh_tokens.items()
            if data.expires_at < now
        ]
        for token in expired_refresh_tokens:
            del self.refresh_tokens[token]

# Global OAuth2 PKCE manager instance
oauth2_manager = OAuth2PKCEManager()

# Request/Response Models for FastAPI
class AuthorizationRequest(BaseModel):
    response_type: str = "code"
    client_id: str
    redirect_uri: str
    scope: str
    code_challenge: str
    code_challenge_method: str = "S256"
    state: Optional[str] = None

class TokenRequest(BaseModel):
    grant_type: str
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    client_id: str
    code_verifier: Optional[str] = None
    refresh_token: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

class PKCEChallengeResponse(BaseModel):
    code_challenge: str
    code_challenge_method: str
    challenge_id: str
    state: str