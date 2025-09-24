from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ContentAssetBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: str
    category: str
    status: str = "Draft"
    tags: List[str] = []
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    author: Optional[str] = None
    seo_keywords: List[str] = []
    seo_description: Optional[str] = None

class ContentAssetCreate(ContentAssetBase):
    pass

class ContentAssetUpdate(ContentAssetBase):
    pass

class ContentAsset(ContentAssetBase):
    id: int
    view_count: int = 0
    download_count: int = 0
    engagement_score: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class ContentPersonalizationBase(BaseModel):
    content_id: int
    segment_id: int
    personalized_content: str  # JSON structure for personalized content
    is_active: bool = True

class ContentPersonalizationCreate(ContentPersonalizationBase):
    pass

class ContentPersonalizationUpdate(ContentPersonalizationBase):
    pass

class ContentPersonalization(ContentPersonalizationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str = "Draft"
    featured_image_url: Optional[str] = None
    tags: List[str] = []
    author: Optional[str] = None
    seo_keywords: List[str] = []
    seo_description: Optional[str] = None
    published_at: Optional[datetime] = None

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    view_count: int = 0
    comment_count: int = 0
    like_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None