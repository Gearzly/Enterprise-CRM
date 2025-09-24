from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SocialPostBase(BaseModel):
    platform: str
    content: str
    media_urls: List[str] = []
    status: str = "Draft"
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    tags: List[str] = []

class SocialPostCreate(SocialPostBase):
    pass

class SocialPostUpdate(SocialPostBase):
    pass

class SocialPost(SocialPostBase):
    id: int
    engagement_count: int = 0
    like_count: int = 0
    share_count: int = 0
    comment_count: int = 0
    view_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class SocialListeningKeywordBase(BaseModel):
    keyword: str
    platform: str
    is_active: bool = True

class SocialListeningKeywordCreate(SocialListeningKeywordBase):
    pass

class SocialListeningKeywordUpdate(SocialListeningKeywordBase):
    pass

class SocialListeningKeyword(SocialListeningKeywordBase):
    id: int
    mention_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

class SocialMentionBase(BaseModel):
    keyword_id: int
    platform: str
    post_id: str  # Platform-specific post ID
    content: str
    author: str
    author_profile_url: Optional[str] = None
    post_url: str
    sentiment: Optional[str] = None  # positive, negative, neutral
    is_responded: bool = False

class SocialMentionCreate(SocialMentionBase):
    pass

class SocialMentionUpdate(SocialMentionBase):
    pass

class SocialMention(SocialMentionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SocialEngagementBase(BaseModel):
    post_id: int
    engagement_type: str
    user_id: Optional[str] = None
    timestamp: datetime

class SocialEngagementCreate(SocialEngagementBase):
    pass

class SocialEngagementUpdate(SocialEngagementBase):
    pass

class SocialEngagement(SocialEngagementBase):
    id: int

class InfluencerBase(BaseModel):
    name: str
    platform: str
    profile_url: str
    followers_count: int
    engagement_rate: float
    category: str
    contact_info: Optional[str] = None
    notes: Optional[str] = None

class InfluencerCreate(InfluencerBase):
    pass

class InfluencerUpdate(InfluencerBase):
    pass

class Influencer(InfluencerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None