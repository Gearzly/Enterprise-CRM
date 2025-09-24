from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Removed Enum import since we're removing static enums

# Removed CommunityPostType enum
# Removed CommunityPostStatus enum

class CommunityCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CommunityCategoryCreate(CommunityCategoryBase):
    pass

class CommunityCategoryUpdate(CommunityCategoryBase):
    pass

class CommunityCategory(CommunityCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class CommunityPostBase(BaseModel):
    title: str
    content: str
    category_id: int
    post_type: str = "Discussion"  # Changed from CommunityPostType to str
    author_id: int
    tags: List[str] = []

class CommunityPostCreate(CommunityPostBase):
    pass

class CommunityPostUpdate(CommunityPostBase):
    pass

class CommunityPost(CommunityPostBase):
    id: int
    status: str = "Published"  # Changed from CommunityPostStatus to str
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0

class CommunityCommentBase(BaseModel):
    post_id: int
    author_id: int
    content: str
    parent_comment_id: Optional[int] = None

class CommunityCommentCreate(CommunityCommentBase):
    pass

class CommunityComment(CommunityCommentBase):
    id: int
    created_at: datetime
    like_count: int = 0
    is_approved: bool = True

class CommunityUserBase(BaseModel):
    user_id: int
    reputation_score: int = 0
    is_expert: bool = False
    is_moderator: bool = False

class CommunityUserCreate(CommunityUserBase):
    pass

class CommunityUser(CommunityUserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class CommunityBadgeBase(BaseModel):
    name: str
    description: str
    criteria: str

class CommunityBadgeCreate(CommunityBadgeBase):
    pass

class CommunityBadge(CommunityBadgeBase):
    id: int
    created_at: datetime