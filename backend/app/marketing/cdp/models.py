from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DataSourceType(str, Enum):
    crm = "CRM"
    website = "Website"
    email = "Email"
    social_media = "Social Media"
    mobile_app = "Mobile App"
    offline = "Offline"
    third_party = "Third Party"
    other = "Other"

class IdentityResolutionStatus(str, Enum):
    pending = "Pending"
    matched = "Matched"
    merged = "Merged"
    conflicted = "Conflicted"

class DataPrivacyStatus(str, Enum):
    compliant = "Compliant"
    pending_consent = "Pending Consent"
    restricted = "Restricted"
    deleted = "Deleted"

class CustomerDataProfileBase(BaseModel):
    customer_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    preferences: Dict[str, Any] = {}  # JSON structure for customer preferences
    tags: List[str] = []
    data_sources: List[str] = []  # List of source system identifiers

class CustomerDataProfileCreate(CustomerDataProfileBase):
    pass

class CustomerDataProfileUpdate(CustomerDataProfileBase):
    pass

class CustomerDataProfile(CustomerDataProfileBase):
    id: int
    profile_score: int = 0
    engagement_score: int = 0
    lifetime_value: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class DataIntegrationBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: DataSourceType
    connection_details: Dict[str, Any]  # JSON structure for connection details
    is_active: bool = True
    sync_frequency: str = "daily"  # hourly, daily, weekly, monthly
    last_sync: Optional[datetime] = None

class DataIntegrationCreate(DataIntegrationBase):
    pass

class DataIntegrationUpdate(DataIntegrationBase):
    pass

class DataIntegration(DataIntegrationBase):
    id: int
    records_processed: int = 0
    last_sync_status: str = "Success"  # Success, Failed, In Progress
    created_at: datetime
    updated_at: Optional[datetime] = None

class IdentityResolutionBase(BaseModel):
    primary_profile_id: int
    duplicate_profile_id: int
    confidence_score: float  # 0.0 to 1.0
    resolution_status: IdentityResolutionStatus = IdentityResolutionStatus.pending
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None

class IdentityResolutionCreate(IdentityResolutionBase):
    pass

class IdentityResolutionUpdate(IdentityResolutionBase):
    pass

class IdentityResolution(IdentityResolutionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class RealTimeSegmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: Dict[str, Any]  # JSON structure for segment criteria
    is_active: bool = True
    member_count: int = 0

class RealTimeSegmentCreate(RealTimeSegmentBase):
    pass

class RealTimeSegmentUpdate(RealTimeSegmentBase):
    pass

class RealTimeSegment(RealTimeSegmentBase):
    id: int
    last_updated: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

class DataPrivacyBase(BaseModel):
    customer_profile_id: int
    consent_status: str = "Granted"  # Granted, Revoked, Pending
    consent_date: Optional[datetime] = None
    consent_source: str  # e.g., "Website Form", "Email", "Phone Call"
    data_processing_purposes: List[str] = []
    restriction_notes: Optional[str] = None
    privacy_status: DataPrivacyStatus = DataPrivacyStatus.compliant

class DataPrivacyCreate(DataPrivacyBase):
    pass

class DataPrivacyUpdate(DataPrivacyBase):
    pass

class DataPrivacy(DataPrivacyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class DataQualityBase(BaseModel):
    customer_profile_id: int
    completeness_score: float = 0.0  # 0.0 to 1.0
    accuracy_score: float = 0.0  # 0.0 to 1.0
    consistency_score: float = 0.0  # 0.0 to 1.0
    freshness_score: float = 0.0  # 0.0 to 1.0
    overall_score: float = 0.0  # 0.0 to 1.0
    issues: List[str] = []
    last_validated: Optional[datetime] = None

class DataQualityCreate(DataQualityBase):
    pass

class DataQualityUpdate(DataQualityBase):
    pass

class DataQuality(DataQualityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None