from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed SocialPlatform enum
# Removed SocialPostStatus enum
# Removed SocialSentiment enum

class SocialInquiryBase(BaseModel):
    customer_id: int
    platform: str  # Changed from SocialPlatform to str
    post_id: str
    content: str
    sentiment: str = "Neutral"  # Changed from SocialSentiment to str
    assigned_agent_id: Optional[str] = None
    tags: List[str] = []

class SocialInquiryCreate(SocialInquiryBase):
    pass

class SocialInquiryUpdate(SocialInquiryBase):
    pass

class SocialInquiry(SocialInquiryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None

class SocialResponseBase(BaseModel):
    inquiry_id: int
    content: str
    created_by: str

class SocialResponseCreate(SocialResponseBase):
    pass

class SocialResponse(SocialResponseBase):
    id: int
    created_at: datetime
    is_published: bool = False
    published_at: Optional[datetime] = None

class SocialTemplateBase(BaseModel):
    name: str
    content: str
    platform: str  # Changed from SocialPlatform to str
    is_active: bool = True

class SocialTemplateCreate(SocialTemplateBase):
    pass

class SocialTemplateUpdate(SocialTemplateBase):
    pass

class SocialTemplate(SocialTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None