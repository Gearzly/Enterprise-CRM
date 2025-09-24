"""
API Routers for Production Security Features

This module provides FastAPI endpoints for production security operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from .production import (
    secret_manager,
    certificate_manager,
    key_rotation_manager,
    get_secret,
    encrypt_secret,
    decrypt_secret,
    encrypt_with_public_key,
    decrypt_with_private_key,
    rotate_all_keys,
    validate_environment_secrets,
    PRODUCTION_SECURITY_CONFIG
)

# Create routers
production_security_router = APIRouter(prefix="/production-security", tags=["Production Security"])

class SecretRequest(BaseModel):
    """Request model for secret operations"""
    key: str
    value: str
    encrypt: bool = True

class SecretResponse(BaseModel):
    """Response model for secret operations"""
    key: str
    value: Optional[str] = None
    encrypted_value: Optional[str] = None
    operation: str

class EncryptionRequest(BaseModel):
    """Request model for encryption operations"""
    data: str

class EncryptionResponse(BaseModel):
    """Response model for encryption operations"""
    original_data: str
    encrypted_data: str

class DecryptionRequest(BaseModel):
    """Request model for decryption operations"""
    encrypted_data: str

class DecryptionResponse(BaseModel):
    """Response model for decryption operations"""
    encrypted_data: str
    decrypted_data: str

class KeyRotationResponse(BaseModel):
    """Response model for key rotation operations"""
    message: str
    details: Dict[str, Any]

class EnvironmentValidationResponse(BaseModel):
    """Response model for environment validation"""
    validation_results: Dict[str, bool]
    missing_secrets: List[str]
    security_config: Dict[str, Any]

# Secret Management Endpoints
@production_security_router.post("/secrets", response_model=SecretResponse)
async def set_secret(request: SecretRequest):
    """Set a secret value"""
    try:
        if request.value:
            secret_manager.set_secret(request.key, request.value, request.encrypt)
            encrypted_value = encrypt_secret(request.value) if request.encrypt else None
        else:
            raise HTTPException(status_code=400, detail="Value is required")
        return SecretResponse(
            key=request.key,
            value=request.value if not request.encrypt else None,
            encrypted_value=encrypted_value,
            operation="set"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@production_security_router.get("/secrets/{key}", response_model=SecretResponse)
async def get_secret_endpoint(key: str, decrypt: bool = True):
    """Get a secret value"""
    try:
        value = get_secret(key)
        if value and decrypt:
            # If it's an encrypted secret, decrypt it
            if key.endswith('_ENCRYPTED'):
                decrypted_value = decrypt_secret(value)
                return SecretResponse(
                    key=key,
                    value=decrypted_value,
                    encrypted_value=value,
                    operation="get_decrypted"
                )
        
        return SecretResponse(
            key=key,
            value=value,
            operation="get"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Encryption/Decryption Endpoints
@production_security_router.post("/encrypt", response_model=EncryptionResponse)
async def encrypt_data(request: EncryptionRequest):
    """Encrypt data with the secret encryption key"""
    try:
        encrypted_data = encrypt_secret(request.data)
        return EncryptionResponse(
            original_data=request.data,
            encrypted_data=encrypted_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@production_security_router.post("/decrypt", response_model=DecryptionResponse)
async def decrypt_data(request: DecryptionRequest):
    """Decrypt data with the secret encryption key"""
    try:
        decrypted_data = decrypt_secret(request.encrypted_data)
        return DecryptionResponse(
            encrypted_data=request.encrypted_data,
            decrypted_data=decrypted_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Certificate-Based Encryption Endpoints
@production_security_router.post("/certificate/encrypt", response_model=EncryptionResponse)
async def encrypt_with_certificate(request: EncryptionRequest):
    """Encrypt data with the public key"""
    try:
        encrypted_data = encrypt_with_public_key(request.data)
        return EncryptionResponse(
            original_data=request.data,
            encrypted_data=encrypted_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@production_security_router.get("/certificate/public-key")
async def get_public_key():
    """Get the public key in PEM format"""
    try:
        public_key_pem = certificate_manager.get_public_key_pem()
        return {"public_key_pem": public_key_pem}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Key Rotation Endpoints
@production_security_router.post("/key-rotation", response_model=KeyRotationResponse)
async def rotate_keys():
    """Rotate all encryption keys"""
    try:
        result = rotate_all_keys()
        return KeyRotationResponse(
            message="Key rotation completed successfully",
            details=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@production_security_router.post("/key-rotation/encryption", response_model=KeyRotationResponse)
async def rotate_encryption_key():
    """Rotate only the encryption key"""
    try:
        new_key = key_rotation_manager.rotate_encryption_key()
        return KeyRotationResponse(
            message="Encryption key rotated successfully",
            details={"encryption_key": new_key}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@production_security_router.post("/key-rotation/certificate", response_model=KeyRotationResponse)
async def rotate_certificate_keys():
    """Rotate certificate keys"""
    try:
        result = key_rotation_manager.rotate_certificate_keys()
        key_rotation_manager.schedule_key_rotation()
        return KeyRotationResponse(
            message="Certificate keys rotated successfully",
            details=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Environment Validation Endpoints
@production_security_router.get("/validate-environment", response_model=EnvironmentValidationResponse)
async def validate_environment():
    """Validate that required secrets are present in environment"""
    try:
        validation_results = validate_environment_secrets()
        missing_secrets = [key for key, present in validation_results.items() if not present]
        return EnvironmentValidationResponse(
            validation_results=validation_results,
            missing_secrets=missing_secrets,
            security_config=PRODUCTION_SECURITY_CONFIG
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Security Configuration Endpoint
@production_security_router.get("/config")
async def get_production_security_config():
    """Get production security configuration"""
    return PRODUCTION_SECURITY_CONFIG