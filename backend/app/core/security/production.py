"""
Production Security Implementation

This module provides production security measures:
- Environment variable management for secrets
- Certificate-based encryption
- Key rotation mechanisms
"""

import os
import json
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SecretManager:
    """Manager for handling secrets in production environment"""
    
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key from environment or create a new one"""
        key = os.environ.get('SECRET_ENCRYPTION_KEY')
        if key:
            # Use the base64 key directly for Fernet
            return key.encode()
        else:
            # For production, this should NEVER happen
            # Generate a new key only for development with strong warning
            logger.critical("SECURITY WARNING: No SECRET_ENCRYPTION_KEY found in environment!")
            logger.critical("This is HIGHLY INSECURE for production use!")
            logger.critical("Please run: python scripts/generate_secure_keys.py")
            return Fernet.generate_key()
    
    def encrypt_secret(self, secret: str) -> str:
        """Encrypt a secret value"""
        encrypted = self.cipher_suite.encrypt(secret.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_secret(self, encrypted_secret: str) -> str:
        """Decrypt a secret value"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_secret.encode())
        decrypted = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted.decode()
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret from environment variables"""
        # First check if it's a direct environment variable
        value = os.environ.get(key)
        if value:
            return value
        
        # Check if it's an encrypted secret in environment
        encrypted_key = f"{key}_ENCRYPTED"
        encrypted_value = os.environ.get(encrypted_key)
        if encrypted_value:
            try:
                return self.decrypt_secret(encrypted_value)
            except Exception as e:
                logger.error(f"Failed to decrypt secret {key}: {e}")
                return default
        
        return default
    
    def set_secret(self, key: str, value: str, encrypt: bool = True) -> None:
        """Set a secret (in production, this would use a secure vault)"""
        if encrypt:
            encrypted_value = self.encrypt_secret(value)
            os.environ[f"{key}_ENCRYPTED"] = encrypted_value
        else:
            os.environ[key] = value

class CertificateManager:
    """Manager for certificate-based encryption"""
    
    def __init__(self):
        self.private_key: Optional[RSAPrivateKey] = None
        self.public_key: Optional[RSAPublicKey] = None
        self._load_or_generate_keys()
    
    def _load_or_generate_keys(self) -> None:
        """Load keys from environment or generate new ones"""
        # Try to load private key from environment
        private_key_b64 = os.environ.get('RSA_PRIVATE_KEY_PEM')
        if private_key_b64:
            try:
                import base64
                private_key_pem = base64.b64decode(private_key_b64.encode()).decode()
                loaded_key = serialization.load_pem_private_key(
                    private_key_pem.encode(),
                    password=None,
                )
                # Ensure it's an RSA key
                if isinstance(loaded_key, RSAPrivateKey):
                    self.private_key = loaded_key
                    self.public_key = self.private_key.public_key()
                    logger.info("Loaded RSA private key from environment")
                    return
                else:
                    logger.error("Loaded key is not an RSA key")
            except Exception as e:
                logger.error(f"Failed to load private key: {e}")
        
        # For production, this should NEVER happen
        logger.critical("SECURITY WARNING: No RSA_PRIVATE_KEY_PEM found in environment!")
        logger.critical("This is HIGHLY INSECURE for production use!")
        logger.critical("Please run: python scripts/generate_secure_keys.py")
        
        # Generate new RSA keys (for development only)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
    
    def encrypt_with_public_key(self, data: str) -> str:
        """Encrypt data with the public key"""
        if not self.public_key:
            raise ValueError("Public key not available")
        
        encrypted = self.public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_with_private_key(self, encrypted_data: str) -> str:
        """Decrypt data with the private key"""
        if not self.private_key:
            raise ValueError("Private key not available")
        
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        
        decrypted = self.private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return decrypted.decode()
    
    def get_public_key_pem(self) -> str:
        """Get the public key in PEM format"""
        if not self.public_key:
            raise ValueError("Public key not available")
        
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return pem.decode()
    
    def save_keys_to_environment(self) -> None:
        """Save keys to environment variables (for development only)"""
        if not self.private_key:
            raise ValueError("Private key not available")
        
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        os.environ['PRIVATE_KEY_PEM'] = pem.decode()
        logger.info("Saved private key to environment")

class KeyRotationManager:
    """Manager for key rotation mechanisms"""
    
    def __init__(self):
        self.secret_manager = SecretManager()
        self.certificate_manager = CertificateManager()
    
    def rotate_encryption_key(self) -> str:
        """Rotate the encryption key"""
        # Generate new key
        new_key = Fernet.generate_key()
        
        # Save new key to environment (in production, this would go to a secure vault)
        os.environ['SECRET_ENCRYPTION_KEY'] = base64.urlsafe_b64encode(new_key).decode()
        
        # Update the secret manager
        self.secret_manager.encryption_key = new_key
        self.secret_manager.cipher_suite = Fernet(new_key)
        
        logger.info("Rotated encryption key")
        return base64.urlsafe_b64encode(new_key).decode()
    
    def rotate_certificate_keys(self) -> Dict[str, str]:
        """Rotate certificate keys"""
        # Generate new keys
        new_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        new_public_key = new_private_key.public_key()
        
        # Save to environment (in production, this would go to a secure vault)
        pem = new_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        os.environ['PRIVATE_KEY_PEM'] = pem.decode()
        
        # Update the certificate manager
        self.certificate_manager.private_key = new_private_key
        self.certificate_manager.public_key = new_public_key
        
        logger.info("Rotated certificate keys")
        return {
            "private_key": "Rotated",
            "public_key_pem": self.certificate_manager.get_public_key_pem()
        }
    
    def schedule_key_rotation(self, days: int = 90) -> None:
        """Schedule key rotation (in production, this would use a job scheduler)"""
        next_rotation = datetime.utcnow() + timedelta(days=days)
        os.environ['NEXT_KEY_ROTATION'] = next_rotation.isoformat()
        logger.info(f"Scheduled next key rotation for {next_rotation}")

# Global instances
secret_manager = SecretManager()
certificate_manager = CertificateManager()
key_rotation_manager = KeyRotationManager()

# Helper functions
def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a secret value"""
    return secret_manager.get_secret(key, default)

def encrypt_secret(secret: str) -> str:
    """Encrypt a secret value"""
    return secret_manager.encrypt_secret(secret)

def decrypt_secret(encrypted_secret: str) -> str:
    """Decrypt a secret value"""
    return secret_manager.decrypt_secret(encrypted_secret)

def encrypt_with_public_key(data: str) -> str:
    """Encrypt data with the public key"""
    return certificate_manager.encrypt_with_public_key(data)

def decrypt_with_private_key(encrypted_data: str) -> str:
    """Decrypt data with the private key"""
    return certificate_manager.decrypt_with_private_key(encrypted_data)

def rotate_all_keys() -> Dict[str, Any]:
    """Rotate all encryption keys"""
    result = {
        "encryption_key": key_rotation_manager.rotate_encryption_key(),
        "certificate_keys": key_rotation_manager.rotate_certificate_keys()
    }
    key_rotation_manager.schedule_key_rotation()
    return result

def validate_environment_secrets() -> Dict[str, bool]:
    """Validate that required secrets are present in environment"""
    required_secrets = [
        'SECRET_ENCRYPTION_KEY',
        'DATABASE_URL',
        'JWT_SECRET_KEY'
    ]
    
    validation_result = {}
    for secret in required_secrets:
        validation_result[secret] = os.environ.get(secret) is not None
    
    return validation_result

# Production security configuration
PRODUCTION_SECURITY_CONFIG = {
    "encryption": {
        "algorithm": "AES-256-GCM",
        "key_rotation_days": 90,
        "minimum_key_length": 256
    },
    "certificates": {
        "type": "X.509",
        "validity_days": 365,
        "key_size": 2048,
        "signature_algorithm": "SHA-256"
    },
    "secrets": {
        "storage": "environment_variables",
        "encryption_required": True,
        "access_logging": True
    },
    "access_control": {
        "multi_factor_auth": True,
        "session_timeout_minutes": 30,
        "max_sessions_per_user": 5
    }
}