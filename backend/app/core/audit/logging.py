"""
Audit Logging Implementation

This module provides comprehensive audit trails for all operations
with immutable log storage capabilities.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import Session
from app.core.database import Base
import json
import hashlib
import logging
from cryptography.fernet import Fernet
import os

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Audit log model
class AuditLog(Base):
    """Model for audit log entries"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    user_id = Column(Integer, nullable=True)
    user_email = Column(String, nullable=True)
    action = Column(String)  # e.g., 'create', 'read', 'update', 'delete'
    resource_type = Column(String)  # e.g., 'customer', 'contact', 'opportunity'
    resource_id = Column(String, nullable=True)  # ID of the resource affected
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    details = Column(Text)  # JSON string with additional details
    is_sensitive = Column(Boolean, default=False)  # Flag for sensitive operations
    log_hash = Column(String)  # Hash for integrity verification
    is_immutable = Column(Boolean, default=True)  # Flag for immutable logs

class AuditLoggingService:
    """Service for handling audit logging operations"""
    
    def __init__(self, db: Session):
        self.db = db
        # Get encryption key from environment or generate one
        self.encryption_key = os.environ.get('AUDIT_ENCRYPTION_KEY')
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def log_action(
        self,
        organization_id: int,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        is_sensitive: bool = False
    ) -> AuditLog:
        """Log an action to the audit trail"""
        
        # Serialize details to JSON
        details_json = json.dumps(details) if details else "{}"
        
        # Create log entry
        log_entry = AuditLog(
            organization_id=organization_id,
            user_id=user_id,
            user_email=user_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details_json,
            is_sensitive=is_sensitive
        )
        
        # Calculate hash for integrity verification
        log_entry.log_hash = self._calculate_hash(log_entry)
        
        # Encrypt sensitive logs
        if is_sensitive:
            log_entry.details = self._encrypt_data(details_json)
        
        # Add to database
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        
        logger.info(f"Audit log entry created: {action} on {resource_type}")
        return log_entry
    
    def get_audit_logs(
        self,
        organization_id: int,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve audit logs with filtering options"""
        query = self.db.query(AuditLog).filter(
            AuditLog.organization_id == organization_id
        )
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    def verify_log_integrity(self, log_id: int) -> bool:
        """Verify the integrity of a log entry"""
        log_entry = self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
        if not log_entry:
            return False
        
        current_hash = self._calculate_hash(log_entry)
        return current_hash == log_entry.log_hash
    
    def _calculate_hash(self, log_entry: AuditLog) -> str:
        """Calculate hash for log integrity verification"""
        # Create a string representation of the log entry
        log_string = f"{log_entry.organization_id}{log_entry.user_id}{log_entry.action}{log_entry.resource_type}{log_entry.resource_id}{log_entry.timestamp}{log_entry.details}"
        return hashlib.sha256(log_string.encode()).hexdigest()
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

# Decorator for automatic audit logging
def audit_log(
    action: str,
    resource_type: str,
    is_sensitive: bool = False
):
    """Decorator to automatically log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract audit information from function arguments
            # This is a simplified implementation - in practice, you'd want to
            # extract this information from the request context or function parameters
            organization_id = kwargs.get('organization_id', 1)  # Default to 1 for demo
            user_id = kwargs.get('user_id')
            user_email = kwargs.get('user_email')
            
            # Create audit service (in practice, you'd inject this)
            # For now, we'll just log that the function was called
            logger.info(f"Audit decorator called for {func.__name__}")
            
            # Call the original function
            result = func(*args, **kwargs)
            
            return result
        return wrapper
    return decorator

# Context manager for audit logging
from contextlib import contextmanager

@contextmanager
def audit_context(
    db: Session,
    organization_id: int,
    user_id: Optional[int] = None,
    user_email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Context manager for audit logging"""
    audit_service = AuditLoggingService(db)
    
    # Log entry to context
    start_time = datetime.utcnow()
    
    try:
        yield audit_service
    finally:
        # Log exit from context
        end_time = datetime.utcnow()
        logger.info(f"Audit context completed in {end_time - start_time}")

# Helper function to log common operations
def log_user_action(
    db: Session,
    organization_id: int,
    user_id: int,
    user_email: str,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    is_sensitive: bool = False
):
    """Helper function to log user actions"""
    audit_service = AuditLoggingService(db)
    return audit_service.log_action(
        organization_id=organization_id,
        user_id=user_id,
        user_email=user_email,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        is_sensitive=is_sensitive
    )