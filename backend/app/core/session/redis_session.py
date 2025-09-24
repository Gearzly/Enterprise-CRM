"""
Redis-based session storage for scalable and persistent session management.
Provides secure session handling with automatic expiration and encryption.
"""
import json
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import base64
import os

import redis
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from ..superadmin.models import User

load_dotenv()
logger = logging.getLogger(__name__)


class RedisSessionManager:
    """Redis-based session management with encryption"""
    
    def __init__(self):
        # Redis connection configuration
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Encryption for session data
        session_key = os.getenv("SESSION_SECRET_KEY")
        if not session_key:
            raise ValueError("SESSION_SECRET_KEY environment variable is not set")
        
        # Create Fernet key from session secret
        import hashlib
        key_bytes = hashlib.sha256(session_key.encode()).digest()
        self.fernet_key = base64.urlsafe_b64encode(key_bytes[:32])
        self.cipher_suite = Fernet(self.fernet_key)
        
        # Default session settings
        self.default_expire_seconds = int(os.getenv("SESSION_EXPIRE_SECONDS", "86400"))  # 24 hours
        self.session_prefix = "crm_session:"
        self.user_sessions_prefix = "user_sessions:"
        
        logger.info("Redis session manager initialized")
    
    def create_session(self, user: User, device_info: Optional[Dict[str, Any]] = None, 
                      expire_seconds: Optional[int] = None) -> str:
        """Create a new session for a user"""
        try:
            session_id = self._generate_session_id()
            expire_time = expire_seconds or self.default_expire_seconds
            expires_at = datetime.utcnow() + timedelta(seconds=expire_time)
            
            session_data = {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": expires_at.isoformat(),
                "device_info": device_info or {},
                "last_activity": datetime.utcnow().isoformat()
            }
            
            # Encrypt session data
            encrypted_data = self._encrypt_data(session_data)
            
            # Store in Redis with expiration
            session_key = f"{self.session_prefix}{session_id}"\n            self.redis_client.setex(session_key, expire_time, encrypted_data)
            
            # Track user sessions for management
            self._add_user_session(user.id, session_id, expire_time)
            
            logger.info(f"Created session {session_id} for user {user.email}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session for user {user.email}: {str(e)}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        try:
            session_key = f"{self.session_prefix}{session_id}"
            encrypted_data = self.redis_client.get(session_key)
            
            if not encrypted_data:
                return None
            
            # Decrypt and return session data
            session_data = self._decrypt_data(encrypted_data)
            
            # Check if session is expired
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            if datetime.utcnow() > expires_at:
                self.delete_session(session_id)
                return None
            
            # Update last activity
            session_data["last_activity"] = datetime.utcnow().isoformat()
            self._update_session_data(session_id, session_data)
            
            return session_data
            
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {str(e)}")
            return None
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data"""
        try:
            session_data = self.get_session(session_id)
            if not session_data:
                return False
            
            # Update data
            session_data.update(data)
            session_data["last_activity"] = datetime.utcnow().isoformat()
            
            return self._update_session_data(session_id, session_data)
            
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {str(e)}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            session_data = self.get_session(session_id)
            
            # Remove from Redis
            session_key = f"{self.session_prefix}{session_id}"
            result = self.redis_client.delete(session_key)
            
            # Remove from user sessions tracking
            if session_data:
                self._remove_user_session(session_data["user_id"], session_id)
            
            logger.info(f"Deleted session {session_id}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {str(e)}")
            return False
    
    def delete_user_sessions(self, user_id: int) -> int:
        """Delete all sessions for a user"""
        try:
            user_sessions = self.get_user_sessions(user_id)
            deleted_count = 0
            
            for session_id in user_sessions:
                if self.delete_session(session_id):
                    deleted_count += 1
            
            # Clear user sessions tracking
            user_sessions_key = f"{self.user_sessions_prefix}{user_id}"
            self.redis_client.delete(user_sessions_key)
            
            logger.info(f"Deleted {deleted_count} sessions for user {user_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to delete sessions for user {user_id}: {str(e)}")
            return 0
    
    def get_user_sessions(self, user_id: int) -> List[str]:
        """Get all session IDs for a user"""
        try:
            user_sessions_key = f"{self.user_sessions_prefix}{user_id}"
            sessions = self.redis_client.smembers(user_sessions_key)
            return list(sessions)
            
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {str(e)}")
            return []
    
    def extend_session(self, session_id: str, additional_seconds: int = None) -> bool:
        """Extend session expiration time"""
        try:
            session_data = self.get_session(session_id)
            if not session_data:
                return False
            
            # Calculate new expiration
            additional_time = additional_seconds or self.default_expire_seconds
            new_expires_at = datetime.utcnow() + timedelta(seconds=additional_time)
            session_data["expires_at"] = new_expires_at.isoformat()
            
            # Update session with new expiration
            session_key = f"{self.session_prefix}{session_id}"
            encrypted_data = self._encrypt_data(session_data)
            self.redis_client.setex(session_key, additional_time, encrypted_data)
            
            logger.info(f"Extended session {session_id} by {additional_time} seconds")
            return True
            
        except Exception as e:
            logger.error(f"Failed to extend session {session_id}: {str(e)}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions (run periodically)"""
        try:
            cleaned_count = 0
            pattern = f"{self.session_prefix}*"
            
            for key in self.redis_client.scan_iter(match=pattern):
                try:
                    session_id = key.replace(self.session_prefix, "")
                    session_data = self.get_session(session_id)
                    
                    if not session_data:  # Session was expired and deleted
                        cleaned_count += 1
                        
                except Exception:
                    # If we can't decrypt or parse, delete the session
                    self.redis_client.delete(key)
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} expired sessions")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {str(e)}")
            return 0
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            total_sessions = len(list(self.redis_client.scan_iter(match=f"{self.session_prefix}*")))
            
            # Get active users count
            active_users = len(list(self.redis_client.scan_iter(match=f"{self.user_sessions_prefix}*")))
            
            # Redis info
            redis_info = self.redis_client.info()
            
            return {
                "total_sessions": total_sessions,
                "active_users": active_users,
                "redis_memory_used": redis_info.get("used_memory_human", "N/A"),
                "redis_connected_clients": redis_info.get("connected_clients", 0),
                "session_prefix": self.session_prefix,
                "default_expire_seconds": self.default_expire_seconds
            }
            
        except Exception as e:
            logger.error(f"Failed to get session stats: {str(e)}")
            return {}
    
    def validate_session_token(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate a session token and return session data"""
        if not session_token:
            return None
        
        try:
            # Extract session ID from token (could be encoded/signed)
            session_id = self._decode_session_token(session_token)
            return self.get_session(session_id)
            
        except Exception as e:
            logger.error(f"Failed to validate session token: {str(e)}")
            return None
    
    def create_session_token(self, session_id: str) -> str:
        """Create a session token from session ID"""
        # In production, you might want to sign this token
        return self._encode_session_token(session_id)
    
    def _generate_session_id(self) -> str:
        """Generate a secure session ID"""
        return secrets.token_urlsafe(32)
    
    def _encrypt_data(self, data: Dict[str, Any]) -> str:
        """Encrypt session data"""
        json_data = json.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt session data"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return json.loads(decrypted_data.decode())
    
    def _update_session_data(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Update session data in Redis"""
        try:
            session_key = f"{self.session_prefix}{session_id}"
            
            # Calculate remaining TTL
            ttl = self.redis_client.ttl(session_key)
            if ttl <= 0:
                return False  # Session expired
            
            # Update with same TTL
            encrypted_data = self._encrypt_data(session_data)
            self.redis_client.setex(session_key, ttl, encrypted_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update session data for {session_id}: {str(e)}")
            return False
    
    def _add_user_session(self, user_id: int, session_id: str, expire_seconds: int):
        """Add session to user's session tracking"""
        try:
            user_sessions_key = f"{self.user_sessions_prefix}{user_id}"
            self.redis_client.sadd(user_sessions_key, session_id)
            self.redis_client.expire(user_sessions_key, expire_seconds + 3600)  # Extra buffer
            
        except Exception as e:
            logger.error(f"Failed to add user session tracking: {str(e)}")
    
    def _remove_user_session(self, user_id: int, session_id: str):
        """Remove session from user's session tracking"""
        try:
            user_sessions_key = f"{self.user_sessions_prefix}{user_id}"
            self.redis_client.srem(user_sessions_key, session_id)
            
        except Exception as e:
            logger.error(f"Failed to remove user session tracking: {str(e)}")
    
    def _encode_session_token(self, session_id: str) -> str:
        """Encode session ID into a token"""
        # Simple base64 encoding - in production, consider JWT or signed tokens
        return base64.urlsafe_b64encode(session_id.encode()).decode()
    
    def _decode_session_token(self, session_token: str) -> str:
        """Decode session token to get session ID"""
        try:
            return base64.urlsafe_b64decode(session_token.encode()).decode()
        except Exception:
            raise ValueError("Invalid session token format")
    
    def health_check(self) -> bool:
        """Check if Redis connection is healthy"""
        try:
            self.redis_client.ping()
            return True
        except Exception:
            return False


# Global session manager instance
session_manager = RedisSessionManager()


# FastAPI dependency for session management
async def get_session_manager() -> RedisSessionManager:
    """Dependency to get session manager"""
    if not session_manager.health_check():
        raise Exception("Redis session store is not available")
    return session_manager


# Session utilities
def create_user_session(user: User, device_info: Optional[Dict[str, Any]] = None) -> str:
    """Utility function to create a session for a user"""
    return session_manager.create_session(user, device_info)


def invalidate_user_session(session_id: str) -> bool:
    """Utility function to invalidate a session"""
    return session_manager.delete_session(session_id)


def get_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Utility function to get session data"""
    return session_manager.get_session(session_id)


def extend_user_session(session_id: str, additional_seconds: int = None) -> bool:
    """Utility function to extend a session"""
    return session_manager.extend_session(session_id, additional_seconds)


def cleanup_user_sessions(user_id: int) -> int:
    """Utility function to cleanup all sessions for a user"""
    return session_manager.delete_user_sessions(user_id)