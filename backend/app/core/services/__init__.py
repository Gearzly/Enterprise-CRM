"""
Core Services Package
Contains shared service modules to avoid circular imports and provide centralized business logic.
"""

from .user_service import user_service, UserService

__all__ = [
    "user_service",
    "UserService",
]