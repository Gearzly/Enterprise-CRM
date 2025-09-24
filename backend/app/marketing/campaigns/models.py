from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    status: str = "Draft"
    start_date: datetime
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    assigned_to: Optional[str] = None
    tags: List[str] = []

    @validator('status')
    def validate_status(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

    @validator('type')
    def validate_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

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
    type: str
    content: str  # JSON template content
    is_active: bool = True

    @validator('type')
    def validate_type(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

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

    @validator('test_metric')
    def validate_test_metric(cls, v):
        # In a real implementation, this would fetch from config
        # For now, we'll allow any string but validate against known values in the service layer
        return v

class ABTestCreate(ABTestBase):
    pass

class ABTestUpdate(ABTestBase):
    pass

class ABTest(ABTestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None