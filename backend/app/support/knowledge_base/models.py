from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ArticleCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class ArticleCategoryCreate(ArticleCategoryBase):
    pass

class ArticleCategoryUpdate(ArticleCategoryBase):
    pass

class ArticleCategory(ArticleCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ArticleBase(BaseModel):
    title: str
    content: str
    category_id: int
    is_published: bool = False
    tags: List[str] = []

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    view_count: int = 0
    helpful_count: int = 0
    not_helpful_count: int = 0

class ArticleFeedbackBase(BaseModel):
    article_id: int
    is_helpful: bool
    comment: Optional[str] = None

class ArticleFeedbackCreate(ArticleFeedbackBase):
    pass

class ArticleFeedback(ArticleFeedbackBase):
    id: int
    created_at: datetime