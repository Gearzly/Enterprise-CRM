"""
User Service Module
Provides user-related operations to avoid circular imports between auth and middleware modules.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.deps import get_db
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """Service class for user operations"""
    
    def __init__(self):
        # Initialize with default users - these will be created in the database
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """Initialize default users in memory (to be moved to database)"""
        self.users = {
            "admin@crm.com": {
                "id": 1,
                "email": "admin@crm.com",
                "name": "System Administrator",
                "status": "active",
                "role": "admin",
                "password_hash": pwd_context.hash("AdminPassword123!")
            },
            "test@crm.com": {
                "id": 2,
                "email": "test@crm.com", 
                "name": "Test User",
                "status": "active",
                "role": "user",
                "password_hash": pwd_context.hash("TestPassword123!")
            }
        }
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address.
        """
        user = self.users.get(email)
        if user:
            # Return user without password hash
            return {k: v for k, v in user.items() if k != "password_hash"}
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        """
        for user in self.users.values():
            if user["id"] == user_id:
                # Return user without password hash
                return {k: v for k, v in user.items() if k != "password_hash"}
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password using proper password hashing.
        """
        user = self.users.get(email)
        if not user:
            return None
        
        # Verify password using bcrypt
        if pwd_context.verify(password, user["password_hash"]):
            # Return user without password hash
            return {k: v for k, v in user.items() if k != "password_hash"}
        return None


# Create a global instance for easy access
user_service = UserService()