from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SocialPlatform(str, Enum):
    facebook = "Facebook"
    twitter = "Twitter"
    instagram = "Instagram"
    linkedin = "LinkedIn"
    youtube = "YouTube"
    tiktok = "TikTok"

class SocialPostStatus(str, Enum):
    pending = "Pending"
    published = "Published"
    scheduled = "Scheduled"
    failed = "Failed"

class SocialSentiment(str, Enum):
    positive = "Positive"
    neutral = "Neutral"
    negative = "Negative"

class SocialInquiryBase(BaseModel):
    customer_id: int
    platform: SocialPlatform
    post_id: str
    content: str
    sentiment: SocialSentiment = SocialSentiment.neutral
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
    platform: SocialPlatform
    is_active: bool = True

class SocialTemplateCreate(SocialTemplateBase):
    pass

class SocialTemplateUpdate(SocialTemplateBase):
    pass

class SocialTemplate(SocialTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None