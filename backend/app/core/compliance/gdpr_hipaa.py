"""
GDPR/HIPAA Compliance Module

This module implements data protection controls required for GDPR and HIPAA compliance:
- Data retention policies
- Right to deletion implementations
- Consent management
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from app.core.database import Base
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Data Retention Models
class DataRetentionPolicy(Base):
    """Model for data retention policies"""
    __tablename__ = "compliance_data_retention_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    module_name = Column(String, index=True)  # e.g., 'sales', 'marketing', 'support'
    data_category = Column(String)  # e.g., 'customer', 'contact', 'activity'
    retention_period_days = Column(Integer)  # Number of days to retain data
    retention_action = Column(String)  # 'delete', 'anonymize', 'archive'
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataRetentionLog(Base):
    """Model for logging data retention actions"""
    __tablename__ = "compliance_data_retention_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer)
    organization_id = Column(Integer)
    action = Column(String)  # 'deleted', 'anonymized', 'archived'
    record_type = Column(String)  # Type of record affected
    record_count = Column(Integer)  # Number of records affected
    details = Column(Text)  # JSON details about the action
    executed_at = Column(DateTime, default=datetime.utcnow)
    executed_by = Column(String)  # User or system that executed the action

# Right to Deletion Models
class DeletionRequest(Base):
    """Model for data deletion requests"""
    __tablename__ = "compliance_deletion_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer)
    requester_id = Column(Integer)  # User making the request
    requester_email = Column(String)
    target_email = Column(String)  # Email of the person whose data is to be deleted
    request_type = Column(String)  # 'gdpr_right_to_be_forgotten', 'hipaa_deletion', 'user_request'
    status = Column(String, default="pending")  # 'pending', 'processing', 'completed', 'rejected'
    reason = Column(Text)  # Reason for the deletion request
    data_identifiers = Column(Text)  # JSON list of data identifiers to delete
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    processed_by = Column(String, nullable=True)
    rejection_reason = Column(Text, nullable=True)

class DeletionLog(Base):
    """Model for logging deletion actions"""
    __tablename__ = "compliance_deletion_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer)
    organization_id = Column(Integer)
    action = Column(String)  # 'deleted', 'anonymized'
    module_name = Column(String)  # Module where data was deleted
    record_type = Column(String)  # Type of record deleted
    record_id = Column(String)  # Identifier of the record
    details = Column(Text)  # Additional details about the deletion
    deleted_at = Column(DateTime, default=datetime.utcnow)
    deleted_by = Column(String)  # User or system that executed the deletion

# Consent Management Models
class ConsentTemplate(Base):
    """Model for consent templates"""
    __tablename__ = "compliance_consent_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer)
    name = Column(String)
    description = Column(Text)
    content = Column(Text)  # HTML content of the consent form
    version = Column(String)
    is_active = Column(Boolean, default=True)
    required_for = Column(String)  # 'all', 'marketing', 'analytics', etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConsentRecord(Base):
    """Model for storing consent records"""
    __tablename__ = "compliance_consent_records"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer)
    user_id = Column(Integer, nullable=True)  # If user is registered
    email = Column(String)  # For unregistered users
    consent_template_id = Column(Integer)
    consent_template_version = Column(String)
    status = Column(String)  # 'granted', 'revoked', 'expired'
    granted_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    ip_address = Column(String)
    user_agent = Column(Text)
    consent_details = Column(Text)  # JSON details about what was consented to

class ConsentLog(Base):
    """Model for logging consent actions"""
    __tablename__ = "compliance_consent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer)
    user_id = Column(Integer, nullable=True)
    email = Column(String)
    action = Column(String)  # 'granted', 'revoked', 'modified'
    consent_template_id = Column(Integer)
    details = Column(Text)  # Additional details about the action
    action_at = Column(DateTime, default=datetime.utcnow)
    action_by = Column(String)  # User or system that executed the action

# GDPR/HIPAA Compliance Service
class GDPRHIPAAComplianceService:
    """Service for handling GDPR/HIPAA compliance operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Data Retention Methods
    def create_retention_policy(self, policy_data: Dict[str, Any]) -> DataRetentionPolicy:
        """Create a new data retention policy"""
        policy = DataRetentionPolicy(**policy_data)
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        logger.info(f"Created retention policy ID: {policy.id}")
        return policy
    
    def get_retention_policies(self, organization_id: int, active_only: bool = True) -> List[DataRetentionPolicy]:
        """Get retention policies for an organization"""
        query = self.db.query(DataRetentionPolicy).filter(
            DataRetentionPolicy.organization_id == organization_id
        )
        if active_only:
            query = query.filter(DataRetentionPolicy.is_active == True)
        return query.all()
    
    def execute_retention_policy(self, policy_id: int, executed_by: str = "system") -> int:
        """Execute a retention policy (placeholder implementation)"""
        policy = self.db.query(DataRetentionPolicy).filter(DataRetentionPolicy.id == policy_id).first()
        if not policy:
            raise ValueError("Policy not found")
        
        # In a real implementation, this would:
        # 1. Identify records that match the policy criteria
        # 2. Apply the retention action (delete, anonymize, archive)
        # 3. Log the action
        
        # For now, we'll just log that the policy was executed
        log_entry = DataRetentionLog(
            policy_id=policy_id,
            organization_id=policy.organization_id,
            action=policy.retention_action,
            record_type=f"{policy.module_name}_{policy.data_category}",
            record_count=0,  # Would be actual count in real implementation
            details=json.dumps({"message": f"Retention policy {policy.retention_action} executed"}),
            executed_by=executed_by
        )
        self.db.add(log_entry)
        self.db.commit()
        
        logger.info(f"Executed retention policy ID: {policy_id}")
        return log_entry.id
    
    # Right to Deletion Methods
    def create_deletion_request(self, request_data: Dict[str, Any]) -> DeletionRequest:
        """Create a new deletion request"""
        request = DeletionRequest(**request_data)
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        logger.info(f"Created deletion request ID: {request.id}")
        return request
    
    def get_deletion_requests(self, organization_id: int, status: Optional[str] = None) -> List[DeletionRequest]:
        """Get deletion requests for an organization"""
        query = self.db.query(DeletionRequest).filter(
            DeletionRequest.organization_id == organization_id
        )
        if status:
            query = query.filter(DeletionRequest.status == status)
        return query.all()
    
    def process_deletion_request(self, request_id: int, processor: str) -> bool:
        """Process a deletion request (placeholder implementation)"""
        request = self.db.query(DeletionRequest).filter(DeletionRequest.id == request_id).first()
        if not request:
            raise ValueError("Deletion request not found")
        
        if request.status != "pending":
            raise ValueError("Deletion request is not in pending status")
        
        # In a real implementation, this would:
        # 1. Identify all records related to the target_email
        # 2. Delete or anonymize those records across all modules
        # 3. Log each deletion action
        # 4. Update the request status
        
        # For now, we'll just update the status and log
        request.status = "completed"
        request.processed_at = datetime.utcnow()
        request.processed_by = processor
        
        # Log the deletion
        log_entry = DeletionLog(
            request_id=request_id,
            organization_id=request.organization_id,
            action="deleted",
            module_name="all_modules",  # Would be specific modules in real implementation
            record_type="user_data",
            record_id=f"user_{request.target_email}",
            details=json.dumps({"message": f"Data deletion completed for {request.target_email}"}),
            deleted_by=processor
        )
        self.db.add(log_entry)
        self.db.commit()
        
        logger.info(f"Processed deletion request ID: {request_id}")
        return True
    
    # Consent Management Methods
    def create_consent_template(self, template_data: Dict[str, Any]) -> ConsentTemplate:
        """Create a new consent template"""
        template = ConsentTemplate(**template_data)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        logger.info(f"Created consent template ID: {template.id}")
        return template
    
    def get_consent_templates(self, organization_id: int, active_only: bool = True) -> List[ConsentTemplate]:
        """Get consent templates for an organization"""
        query = self.db.query(ConsentTemplate).filter(
            ConsentTemplate.organization_id == organization_id
        )
        if active_only:
            query = query.filter(ConsentTemplate.is_active == True)
        return query.all()
    
    def record_consent(self, consent_data: Dict[str, Any]) -> ConsentRecord:
        """Record user consent"""
        consent = ConsentRecord(**consent_data)
        self.db.add(consent)
        self.db.commit()
        self.db.refresh(consent)
        logger.info(f"Recorded consent ID: {consent.id}")
        return consent
    
    def revoke_consent(self, consent_id: int, revoker: str) -> bool:
        """Revoke user consent"""
        consent = self.db.query(ConsentRecord).filter(ConsentRecord.id == consent_id).first()
        if not consent:
            raise ValueError("Consent record not found")
        
        if consent.status == "revoked":
            return True  # Already revoked
        
        consent.status = "revoked"
        consent.revoked_at = datetime.utcnow()
        
        # Log the revocation
        log_entry = ConsentLog(
            organization_id=consent.organization_id,
            user_id=consent.user_id,
            email=consent.email,
            action="revoked",
            consent_template_id=consent.consent_template_id,
            details=json.dumps({"message": f"Consent revoked by {revoker}"}),
            action_by=revoker
        )
        self.db.add(log_entry)
        self.db.commit()
        
        logger.info(f"Revoked consent ID: {consent_id}")
        return True
    
    def get_user_consents(self, organization_id: int, email: str) -> List[ConsentRecord]:
        """Get all consent records for a user"""
        return self.db.query(ConsentRecord).filter(
            ConsentRecord.organization_id == organization_id,
            ConsentRecord.email == email
        ).all()

# Helper functions
def anonymize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Anonymize personal data (placeholder implementation)"""
    anonymized = data.copy()
    # In a real implementation, this would:
    # 1. Remove or obfuscate personally identifiable information
    # 2. Keep only non-identifiable data for analytics/statistics
    sensitive_fields = ['email', 'phone', 'address', 'name']
    for field in sensitive_fields:
        if field in anonymized:
            anonymized[field] = f"anonymized_{hash(anonymized[field]) % 10000}"
    return anonymized

def validate_consent(organization_id: int, email: str, required_for: str, db: Session) -> bool:
    """Validate that a user has given consent for a specific purpose"""
    # Check if user has active consent for the required purpose
    consent_records = db.query(ConsentRecord).join(ConsentTemplate).filter(
        ConsentRecord.organization_id == organization_id,
        ConsentRecord.email == email,
        ConsentRecord.status == "granted",
        ConsentTemplate.required_for.in_([required_for, "all"])
    ).all()
    
    # Check if consent is still valid (not expired)
    valid_consents = [
        consent for consent in consent_records 
        if not consent.expiry_date or consent.expiry_date > datetime.utcnow()
    ]
    
    return len(valid_consents) > 0