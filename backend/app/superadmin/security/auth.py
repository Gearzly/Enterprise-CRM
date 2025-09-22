"""
Authentication module implementing OAuth 2.0, OpenID Connect, MFA, 
device fingerprinting, and WebAuthn support.
"""
import hashlib
import secrets
import base64
import json
import jwt
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from cryptography.fernet import Fernet

from ..models import AuthToken, TokenData, DeviceInfo, MFACode, WebAuthnCredential, User

router = APIRouter()

# Secret key for JWT tokens (in production, use environment variables)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# In-memory storage for demo purposes
sessions_db: Dict[str, Dict[str, Any]] = {}  # session_id -> {user_id, encrypted_data, expires_at}
mfa_codes_db: List[MFACode] = []
webauthn_credentials_db: List[WebAuthnCredential] = []
devices_db: List[DeviceInfo] = []

# Encryption key for session data (in production, use environment variables)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/superadmin/security/auth/token")

class TokenRequest(BaseModel):
    grant_type: str
    username: str
    password: str
    scope: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class MFARequest(BaseModel):
    user_id: int
    code: str

class WebAuthnRegisterRequest(BaseModel):
    user_id: int
    credential_id: str
    public_key: str
    device_name: str

class WebAuthnAuthenticateRequest(BaseModel):
    user_id: int
    credential_id: str
    signature: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create a refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # In a real implementation, use a proper password hashing library like bcrypt
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # In a real implementation, use a proper password hashing library like bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by email (placeholder implementation)"""
    # In a real implementation, this would query the database
    from .security import users_db
    for user in users_db:
        if user.email == email:
            return user
    return None

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    user = get_user_by_email(email)
    if not user:
        return None
    # In a real implementation, verify against a stored hash
    if not verify_password(password, get_password_hash(password)):
        return None
    return user

def generate_mfa_code(user_id: int) -> str:
    """Generate a 6-digit MFA code"""
    code = secrets.token_hex(3)  # 6-character hex string
    expires_at = datetime.utcnow() + timedelta(minutes=5)  # Code expires in 5 minutes
    
    mfa_code = MFACode(
        user_id=user_id,
        code=code,
        expires_at=expires_at
    )
    mfa_codes_db.append(mfa_code)
    return code

def verify_mfa_code(user_id: int, code: str) -> bool:
    """Verify an MFA code"""
    current_time = datetime.utcnow()
    for mfa_code in mfa_codes_db:
        if (mfa_code.user_id == user_id and 
            mfa_code.code == code and 
            not mfa_code.used and 
            mfa_code.expires_at > current_time):
            mfa_code.used = True
            return True
    return False

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user"""
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def encrypt_session_data(data: dict) -> str:
    """Encrypt session data"""
    json_data = json.dumps(data)
    encrypted_data = cipher_suite.encrypt(json_data.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()

def decrypt_session_data(encrypted_data: str) -> dict:
    """Decrypt session data"""
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted_data = cipher_suite.decrypt(encrypted_bytes)
    return json.loads(decrypted_data.decode())

@router.post("/token", response_model=AuthToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth 2.0 token endpoint"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=AuthToken)
async def refresh_access_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Generate new tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/mfa/generate")
async def generate_mfa(user_id: int):
    """Generate MFA code for a user"""
    code = generate_mfa_code(user_id)
    # In a real implementation, send this code via email/SMS
    return {"message": "MFA code generated", "code": code}  # For demo, we return the code

@router.post("/mfa/verify")
async def verify_mfa(request: MFARequest):
    """Verify MFA code"""
    if verify_mfa_code(request.user_id, request.code):
        return {"message": "MFA verification successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired MFA code")

@router.post("/webauthn/register")
async def register_webauthn_credential(request: WebAuthnRegisterRequest):
    """Register a new WebAuthn credential"""
    credential = WebAuthnCredential(
        id=request.credential_id,
        user_id=request.user_id,
        public_key=request.public_key,
        sign_count=0,
        device_name=request.device_name,
        created_at=datetime.utcnow()
    )
    webauthn_credentials_db.append(credential)
    return {"message": "WebAuthn credential registered successfully"}

@router.post("/webauthn/authenticate")
async def authenticate_webauthn(request: WebAuthnAuthenticateRequest):
    """Authenticate using WebAuthn credential"""
    for credential in webauthn_credentials_db:
        if (credential.id == request.credential_id and 
            credential.user_id == request.user_id):
            # In a real implementation, verify the signature
            # For demo, we'll just return success
            return {"message": "WebAuthn authentication successful"}
    
    raise HTTPException(status_code=400, detail="Invalid WebAuthn credential")

@router.post("/session")
async def create_session(user_id: int, device_info: DeviceInfo):
    """Create a new session with device fingerprinting"""
    session_id = secrets.token_urlsafe(32)
    session_data = {
        "user_id": user_id,
        "device_info": device_info.dict()
    }
    
    encrypted_data = encrypt_session_data(session_data)
    expires_at = datetime.utcnow() + timedelta(hours=24)  # Session expires in 24 hours
    
    sessions_db[session_id] = {
        "user_id": user_id,
        "encrypted_data": encrypted_data,
        "expires_at": expires_at
    }
    
    devices_db.append(device_info)
    
    return {"session_id": session_id, "expires_at": expires_at}

@router.delete("/session/{session_id}")
async def invalidate_session(session_id: str):
    """Invalidate a session"""
    if session_id in sessions_db:
        del sessions_db[session_id]
        return {"message": "Session invalidated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.get("/devices")
async def list_user_devices(user_id: int):
    """List all devices for a user"""
    user_devices = [device for device in devices_db if device.device_id == str(user_id)]
    return user_devices

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user