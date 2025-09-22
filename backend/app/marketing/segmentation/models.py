from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SegmentType(str, Enum):
    dynamic = "Dynamic"
    static = "Static"
    account_based = "Account-Based"

class SegmentCriteriaType(str, Enum):
    demographic = "Demographic"
    behavioral = "Behavioral"
    firmographic = "Firmographic"
    technographic = "Technographic"
    custom = "Custom"

class AudienceBase(BaseModel):
    name: str
    description: Optional[str] = None
    segment_type: SegmentType
    criteria: Dict[str, Any]  # JSON structure for segment criteria
    is_active: bool = True
    tags: List[str] = []

class AudienceCreate(AudienceBase):
    pass

class AudienceUpdate(AudienceBase):
    pass

class Audience(AudienceBase):
    id: int
    member_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class SegmentCriteriaBase(BaseModel):
    audience_id: int
    criteria_type: SegmentCriteriaType
    field_name: str
    operator: str  # e.g., "equals", "contains", "greater_than"
    value: str
    logical_operator: Optional[str] = "AND"  # AND, OR

class SegmentCriteriaCreate(SegmentCriteriaBase):
    pass

class SegmentCriteriaUpdate(SegmentCriteriaBase):
    pass

class SegmentCriteria(SegmentCriteriaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class CustomAudienceBase(BaseModel):
    name: str
    description: Optional[str] = None
    member_ids: List[int] = []  # List of contact/lead IDs
    is_active: bool = True

class CustomAudienceCreate(CustomAudienceBase):
    pass

class CustomAudienceUpdate(CustomAudienceBase):
    pass

class CustomAudience(CustomAudienceBase):
    id: int
    member_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class DemographicTargetingBase(BaseModel):
    name: str
    description: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    income_min: Optional[float] = None
    income_max: Optional[float] = None
    is_active: bool = True

class DemographicTargetingCreate(DemographicTargetingBase):
    pass

class DemographicTargetingUpdate(DemographicTargetingBase):
    pass

class DemographicTargeting(DemographicTargetingBase):
    id: int
    target_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class BehavioralTargetingBase(BaseModel):
    name: str
    description: Optional[str] = None
    engagement_score_min: Optional[int] = None
    engagement_score_max: Optional[int] = None
    page_views_min: Optional[int] = None
    page_views_max: Optional[int] = None
    email_opens_min: Optional[int] = None
    email_opens_max: Optional[int] = None
    is_active: bool = True

class BehavioralTargetingCreate(BehavioralTargetingBase):
    pass

class BehavioralTargetingUpdate(BehavioralTargetingBase):
    pass

class BehavioralTargeting(BehavioralTargetingBase):
    id: int
    target_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class AccountBasedMarketingBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_ids: List[int] = []  # List of company/account IDs
    industry: Optional[str] = None
    company_size_min: Optional[int] = None
    company_size_max: Optional[int] = None
    is_active: bool = True

class AccountBasedMarketingCreate(AccountBasedMarketingBase):
    pass

class AccountBasedMarketingUpdate(AccountBasedMarketingBase):
    pass

class AccountBasedMarketing(AccountBasedMarketingBase):
    id: int
    account_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None