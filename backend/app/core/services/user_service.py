"""
User Service Module
Provides user-related operations to avoid circular imports between auth and middleware modules.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.deps import get_db


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address.
        This is a simplified implementation for demo purposes.
        In production, this would query the actual user database.
        """
        # Demo users for testing
        demo_users = {
            "test@example.com": {
                "id": 1, 
                "email": "test@example.com", 
                "name": "Test User", 
                "status": "active",
                "role": "user"
            },
            "testuser@example.com": {
                "id": 2, 
                "email": "testuser@example.com", 
                "name": "Test User 2", 
                "status": "active",
                "role": "user"
            },
            "admin@demo.com": {
                "id": 3, 
                "email": "admin@demo.com", 
                "name": "Admin User", 
                "status": "active",
                "role": "admin"
            }
        }
        
        return demo_users.get(email)
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        This is a simplified implementation for demo purposes.
        """
        # In production, this would query the database by ID
        all_users = [
            {"id": 1, "email": "test@example.com", "name": "Test User", "status": "active", "role": "user"},
            {"id": 2, "email": "testuser@example.com", "name": "Test User 2", "status": "active", "role": "user"},
            {"id": 3, "email": "admin@demo.com", "name": "Admin User", "status": "active", "role": "admin"}
        ]
        
        for user in all_users:
            if user["id"] == user_id:
                return user
        return None
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password.
        This is a simplified implementation for demo purposes.
        """
        user = UserService.get_user_by_email(email)
        if not user:
            return None
        
        # Demo authentication - in production, verify hashed password
        demo_credentials = {
            "test@example.com": "testpassword",
            "testuser@example.com": "testpassword123",
            "admin@demo.com": "adminpassword"
        }
        
        if demo_credentials.get(email) == password:
            return user
        return None


# Create a global instance for easy access
user_service = UserService()