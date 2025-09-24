"""
Data Classification Implementation

This module provides data sensitivity labeling and appropriate handling
based on classification levels.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import Session
from app.core.database import Base
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Data classification levels
class DataClassificationLevel(Enum):
    """Data classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    HIGHLY_RESTRICTED = "highly_restricted"

# Data classification model
class DataClassification(Base):
    """Model for data classification policies"""
    __tablename__ = "data_classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    name = Column(String)  # e.g., "Customer Data", "Financial Records"
    description = Column(Text)
    classification_level = Column(String)  # From DataClassificationLevel
    data_patterns = Column(Text)  # JSON list of regex patterns to identify this data type
    handling_procedures = Column(Text)  # JSON description of handling procedures
    retention_period_days = Column(Integer)  # How long to retain this data
    encryption_required = Column(Boolean, default=False)
    access_control_required = Column(Boolean, default=False)
    audit_logging_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataLabel(Base):
    """Model for labeled data instances"""
    __tablename__ = "data_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    data_type = Column(String)  # e.g., "customer", "contact", "opportunity"
    data_id = Column(String)  # Identifier of the specific data record
    classification_id = Column(Integer)  # Reference to DataClassification
    classification_level = Column(String)  # From DataClassificationLevel
    labeled_at = Column(DateTime, default=datetime.utcnow)
    labeled_by = Column(String)  # User or system that applied the label
    is_active = Column(Boolean, default=True)

class DataClassificationService:
    """Service for handling data classification operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_classification(self, classification_data: Dict[str, Any]) -> DataClassification:
        """Create a new data classification policy"""
        classification = DataClassification(**classification_data)
        self.db.add(classification)
        self.db.commit()
        self.db.refresh(classification)
        logger.info(f"Created data classification ID: {classification.id}")
        return classification
    
    def get_classifications(self, organization_id: int) -> List[DataClassification]:
        """Get all data classifications for an organization"""
        return self.db.query(DataClassification).filter(
            DataClassification.organization_id == organization_id
        ).all()
    
    def classify_data(
        self,
        organization_id: int,
        data_type: str,
        data_id: str,
        data_content: str,
        labeled_by: str
    ) -> DataLabel:
        """Classify a data instance based on content and policies"""
        # Get all classifications for the organization
        classifications = self.get_classifications(organization_id)
        
        # Find the most appropriate classification based on data patterns
        best_match = None
        best_level = None
        
        for classification in classifications:
            # Parse data patterns
            try:
                patterns = json.loads(classification.data_patterns)
            except json.JSONDecodeError:
                continue
            
            # Check if any pattern matches the data content
            for pattern in patterns:
                import re
                if re.search(pattern, data_content, re.IGNORECASE):
                    # Found a match, check if it's a higher classification level
                    current_level = DataClassificationLevel(classification.classification_level)
                    if not best_level or self._is_higher_classification(current_level, best_level):
                        best_match = classification
                        best_level = current_level
                    break
        
        # If no specific classification found, use default (INTERNAL)
        if not best_match:
            classification_level = DataClassificationLevel.INTERNAL.value
            classification_id = None
        else:
            classification_level = best_match.classification_level
            classification_id = best_match.id
        
        # Create data label
        label = DataLabel(
            organization_id=organization_id,
            data_type=data_type,
            data_id=data_id,
            classification_id=classification_id,
            classification_level=classification_level,
            labeled_by=labeled_by
        )
        
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        
        logger.info(f"Classified data {data_type}:{data_id} as {classification_level}")
        return label
    
    def get_data_labels(self, organization_id: int, data_type: Optional[str] = None) -> List[DataLabel]:
        """Get data labels for an organization"""
        query = self.db.query(DataLabel).filter(
            DataLabel.organization_id == organization_id,
            DataLabel.is_active == True
        )
        
        if data_type:
            query = query.filter(DataLabel.data_type == data_type)
        
        return query.all()
    
    def get_handling_procedures(self, classification_id: int) -> Dict[str, Any]:
        """Get handling procedures for a classification"""
        classification = self.db.query(DataClassification).filter(
            DataClassification.id == classification_id
        ).first()
        
        if not classification:
            return {}
        
        try:
            return json.loads(classification.handling_procedures)
        except json.JSONDecodeError:
            return {}
    
    def _is_higher_classification(self, level1: DataClassificationLevel, level2: DataClassificationLevel) -> bool:
        """Check if level1 is a higher classification than level2"""
        level_order = [
            DataClassificationLevel.PUBLIC,
            DataClassificationLevel.INTERNAL,
            DataClassificationLevel.CONFIDENTIAL,
            DataClassificationLevel.RESTRICTED,
            DataClassificationLevel.HIGHLY_RESTRICTED
        ]
        
        try:
            return level_order.index(level1) > level_order.index(level2)
        except ValueError:
            return False

# Helper functions for data classification
def get_classification_requirements(classification_level: str) -> Dict[str, bool]:
    """Get security requirements for a classification level"""
    requirements = {
        "encryption_required": False,
        "access_control_required": False,
        "audit_logging_required": False,
        "multi_factor_auth_required": False
    }
    
    level = DataClassificationLevel(classification_level)
    
    if level == DataClassificationLevel.CONFIDENTIAL:
        requirements["encryption_required"] = True
        requirements["access_control_required"] = True
        requirements["audit_logging_required"] = True
    elif level == DataClassificationLevel.RESTRICTED:
        requirements["encryption_required"] = True
        requirements["access_control_required"] = True
        requirements["audit_logging_required"] = True
        requirements["multi_factor_auth_required"] = True
    elif level == DataClassificationLevel.HIGHLY_RESTRICTED:
        requirements["encryption_required"] = True
        requirements["access_control_required"] = True
        requirements["audit_logging_required"] = True
        requirements["multi_factor_auth_required"] = True
    
    return requirements

def check_data_access_permission(
    user_classification_level: str,
    data_classification_level: str
) -> bool:
    """Check if a user has permission to access data based on classification levels"""
    level_order = [
        DataClassificationLevel.PUBLIC,
        DataClassificationLevel.INTERNAL,
        DataClassificationLevel.CONFIDENTIAL,
        DataClassificationLevel.RESTRICTED,
        DataClassificationLevel.HIGHLY_RESTRICTED
    ]
    
    try:
        user_level_idx = level_order.index(DataClassificationLevel(user_classification_level))
        data_level_idx = level_order.index(DataClassificationLevel(data_classification_level))
        
        # User can access data if their clearance level is equal or higher than data level
        return user_level_idx >= data_level_idx
    except ValueError:
        # If we can't determine levels, deny access
        return False

# Predefined data classification templates
DATA_CLASSIFICATION_TEMPLATES = {
    "customer_data": {
        "name": "Customer Data",
        "description": "Personal information about customers",
        "classification_level": DataClassificationLevel.CONFIDENTIAL.value,
        "data_patterns": json.dumps([
            r"email",
            r"phone",
            r"address",
            r"ssn",
            r"social.security",
            r"credit.card",
            r"bank.account"
        ]),
        "handling_procedures": json.dumps({
            "storage": "Encrypted at rest and in transit",
            "access": "Role-based access control with audit logging",
            "transfer": "Only via secure channels",
            "disposal": "Secure deletion after retention period"
        }),
        "retention_period_days": 3650,  # 10 years
        "encryption_required": True,
        "access_control_required": True,
        "audit_logging_required": True
    },
    "financial_data": {
        "name": "Financial Data",
        "description": "Financial records and transactions",
        "classification_level": DataClassificationLevel.RESTRICTED.value,
        "data_patterns": json.dumps([
            r"account.number",
            r"routing.number",
            r"credit.card",
            r"payment.info",
            r"transaction",
            r"invoice",
            r"billing"
        ]),
        "handling_procedures": json.dumps({
            "storage": "Encrypted at rest and in transit with key rotation",
            "access": "Strict role-based access with MFA and audit logging",
            "transfer": "Only via secure, encrypted channels",
            "disposal": "Secure deletion with certificate of destruction"
        }),
        "retention_period_days": 2555,  # 7 years
        "encryption_required": True,
        "access_control_required": True,
        "audit_logging_required": True
    },
    "health_data": {
        "name": "Health Information",
        "description": "Protected health information (PHI)",
        "classification_level": DataClassificationLevel.HIGHLY_RESTRICTED.value,
        "data_patterns": json.dumps([
            r"medical.record",
            r"health.info",
            r"diagnosis",
            r"treatment",
            r"prescription",
            r"insurance.claim"
        ]),
        "handling_procedures": json.dumps({
            "storage": "Encrypted at rest and in transit with HSM",
            "access": "Need-to-know basis with MFA, audit logging, and regular access reviews",
            "transfer": "Only via HIPAA-compliant secure channels",
            "disposal": "Secure deletion with certificate of destruction and regulatory reporting"
        }),
        "retention_period_days": 3650,  # 10 years
        "encryption_required": True,
        "access_control_required": True,
        "audit_logging_required": True
    }
}