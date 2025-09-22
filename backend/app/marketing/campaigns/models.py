from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CampaignStatus(str, Enum):
    draft = "Draft"
    scheduled = "Scheduled"
    active = "Active"
    paused = "Paused"
    completed = "Completed"
    cancelled = "Cancelled"

class CampaignType(str, Enum):
    email = "Email"
    social_media = "Social Media"
    direct_mail = "Direct Mail"
    ppc = "PPC"
    content = "Content"
    event = "Event"
    other = "Other"

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: CampaignType
    status: CampaignStatus = CampaignStatus.draft
    start_date: datetime
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    assigned_to: Optional[str] = None
    tags: List[str] = []

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class CampaignTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: CampaignType
    content: str  # JSON template content
    is_active: bool = True

class CampaignTemplateCreate(CampaignTemplateBase):
    pass

class CampaignTemplateUpdate(CampaignTemplateBase):
    pass

class CampaignTemplate(CampaignTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ABTestBase(BaseModel):
    name: str
    campaign_id: int
    variant_a_content: str
    variant_b_content: str
    test_metric: str  # e.g., "click_rate", "conversion_rate"
    status: str = "draft"  # draft, running, completed

class ABTestCreate(ABTestBase):
    pass

class ABTestUpdate(ABTestBase):
    pass

class ABTest(ABTestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None