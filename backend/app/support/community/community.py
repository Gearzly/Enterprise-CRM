from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    CommunityCategory, CommunityCategoryCreate, CommunityCategoryUpdate,
    CommunityPost, CommunityPostCreate, CommunityPostUpdate,
    CommunityComment, CommunityCommentCreate,
    CommunityUser, CommunityUserCreate,
    CommunityBadge, CommunityBadgeCreate
)
from .config import (
    get_community_post_types, get_community_post_statuses,
    get_default_post_type, get_default_post_status,
    get_max_tags_per_post, get_reputation_threshold_expert
)

router = APIRouter()

# In-memory storage for demo purposes
community_categories_db = []
community_posts_db = []
community_comments_db = []
community_users_db = []
community_badges_db = []

@router.get("/categories", response_model=List[CommunityCategory])
def list_community_categories():
    """List all community categories"""
    return community_categories_db

@router.get("/categories/{category_id}", response_model=CommunityCategory)
def get_community_category(category_id: int):
    """Get a specific community category by ID"""
    for category in community_categories_db:
        if category.id == category_id:
            return category
    raise HTTPException(status_code=404, detail="Community category not found")

@router.post("/categories", response_model=CommunityCategory)
def create_community_category(category: CommunityCategoryCreate):
    """Create a new community category"""
    new_id = max([c.id for c in community_categories_db]) + 1 if community_categories_db else 1
    new_category = CommunityCategory(
        id=new_id,
        created_at=datetime.now(),
        **category.dict()
    )
    community_categories_db.append(new_category)
    return new_category

@router.put("/categories/{category_id}", response_model=CommunityCategory)
def update_community_category(category_id: int, category_update: CommunityCategoryUpdate):
    """Update an existing community category"""
    for index, category in enumerate(community_categories_db):
        if category.id == category_id:
            updated_category = CommunityCategory(
                id=category_id,
                created_at=category.created_at,
                updated_at=datetime.now(),
                **category_update.dict()
            )
            community_categories_db[index] = updated_category
            return updated_category
    raise HTTPException(status_code=404, detail="Community category not found")

@router.delete("/categories/{category_id}")
def delete_community_category(category_id: int):
    """Delete a community category"""
    for index, category in enumerate(community_categories_db):
        if category.id == category_id:
            del community_categories_db[index]
            return {"message": "Community category deleted successfully"}
    raise HTTPException(status_code=404, detail="Community category not found")

@router.post("/categories/{category_id}/activate")
def activate_community_category(category_id: int):
    """Activate a community category"""
    for index, category in enumerate(community_categories_db):
        if category.id == category_id:
            community_categories_db[index].is_active = True
            return {"message": "Community category activated successfully"}
    raise HTTPException(status_code=404, detail="Community category not found")

@router.post("/categories/{category_id}/deactivate")
def deactivate_community_category(category_id: int):
    """Deactivate a community category"""
    for index, category in enumerate(community_categories_db):
        if category.id == category_id:
            community_categories_db[index].is_active = False
            return {"message": "Community category deactivated successfully"}
    raise HTTPException(status_code=404, detail="Community category not found")

# Community Post endpoints
@router.get("/posts", response_model=List[CommunityPost])
def list_community_posts():
    """List all community posts"""
    return community_posts_db

@router.get("/posts/{post_id}", response_model=CommunityPost)
def get_community_post(post_id: int):
    """Get a specific community post by ID"""
    for post in community_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Community post not found")

@router.post("/posts", response_model=CommunityPost)
def create_community_post(post: CommunityPostCreate):
    """Create a new community post"""
    new_id = max([p.id for p in community_posts_db]) + 1 if community_posts_db else 1
    new_post = CommunityPost(
        id=new_id,
        created_at=datetime.now(),
        **post.dict()
    )
    community_posts_db.append(new_post)
    return new_post

@router.put("/posts/{post_id}", response_model=CommunityPost)
def update_community_post(post_id: int, post_update: CommunityPostUpdate):
    """Update an existing community post"""
    for index, post in enumerate(community_posts_db):
        if post.id == post_id:
            updated_post = CommunityPost(
                id=post_id,
                created_at=post.created_at,
                updated_at=datetime.now(),
                **post_update.dict()
            )
            community_posts_db[index] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Community post not found")

@router.delete("/posts/{post_id}")
def delete_community_post(post_id: int):
    """Delete a community post"""
    for index, post in enumerate(community_posts_db):
        if post.id == post_id:
            community_posts_db[index].status = "Deleted"
            return {"message": "Community post deleted successfully"}
    raise HTTPException(status_code=404, detail="Community post not found")

@router.post("/posts/{post_id}/publish")
def publish_community_post(post_id: int):
    """Publish a community post"""
    for index, post in enumerate(community_posts_db):
        if post.id == post_id:
            community_posts_db[index].status = "Published"
            community_posts_db[index].published_at = datetime.now()
            return {"message": "Community post published successfully"}
    raise HTTPException(status_code=404, detail="Community post not found")

@router.post("/posts/{post_id}/archive")
def archive_community_post(post_id: int):
    """Archive a community post"""
    for index, post in enumerate(community_posts_db):
        if post.id == post_id:
            community_posts_db[index].status = "Archived"
            return {"message": "Community post archived successfully"}
    raise HTTPException(status_code=404, detail="Community post not found")

@router.get("/posts/category/{category_id}", response_model=List[CommunityPost])
def get_posts_by_category(category_id: int):
    """Get community posts by category"""
    return [post for post in community_posts_db if post.category_id == category_id]

@router.get("/posts/author/{author_id}", response_model=List[CommunityPost])
def get_posts_by_author(author_id: int):
    """Get community posts by author"""
    return [post for post in community_posts_db if post.author_id == author_id]

@router.get("/posts/type/{post_type}", response_model=List[CommunityPost])
def get_posts_by_type(post_type: str):
    """Get community posts by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = post_type.lower().title()
    return [post for post in community_posts_db if post.post_type.value == normalized_type]

@router.get("/posts/status/{status}", response_model=List[CommunityPost])
def get_posts_by_status(status: str):
    """Get community posts by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [post for post in community_posts_db if post.status.value == normalized_status]

@router.post("/posts/{post_id}/like")
def like_community_post(post_id: int):
    """Like a community post"""
    for index, post in enumerate(community_posts_db):
        if post.id == post_id:
            community_posts_db[index].like_count += 1
            return {"message": "Community post liked successfully"}
    raise HTTPException(status_code=404, detail="Community post not found")

# Community Comment endpoints
@router.get("/comments", response_model=List[CommunityComment])
def list_community_comments():
    """List all community comments"""
    return community_comments_db

@router.get("/comments/{comment_id}", response_model=CommunityComment)
def get_community_comment(comment_id: int):
    """Get a specific community comment by ID"""
    for comment in community_comments_db:
        if comment.id == comment_id:
            return comment
    raise HTTPException(status_code=404, detail="Community comment not found")

@router.post("/comments", response_model=CommunityComment)
def create_community_comment(comment: CommunityCommentCreate):
    """Create a new community comment"""
    new_id = max([c.id for c in community_comments_db]) + 1 if community_comments_db else 1
    new_comment = CommunityComment(
        id=new_id,
        created_at=datetime.now(),
        **comment.dict()
    )
    community_comments_db.append(new_comment)
    
    # Update comment count on the post
    for post in community_posts_db:
        if post.id == comment.post_id:
            post.comment_count += 1
            break
    
    return new_comment

@router.put("/comments/{comment_id}", response_model=CommunityComment)
def update_community_comment(comment_id: int, comment_update: CommunityCommentCreate):
    """Update an existing community comment"""
    for index, comment in enumerate(community_comments_db):
        if comment.id == comment_id:
            updated_comment = CommunityComment(
                id=comment_id,
                created_at=comment.created_at,
                **comment_update.dict()
            )
            community_comments_db[index] = updated_comment
            return updated_comment
    raise HTTPException(status_code=404, detail="Community comment not found")

@router.delete("/comments/{comment_id}")
def delete_community_comment(comment_id: int):
    """Delete a community comment"""
    for index, comment in enumerate(community_comments_db):
        if comment.id == comment_id:
            del community_comments_db[index]
            return {"message": "Community comment deleted successfully"}
    raise HTTPException(status_code=404, detail="Community comment not found")

@router.get("/posts/{post_id}/comments", response_model=List[CommunityComment])
def get_comments_for_post(post_id: int):
    """Get comments for a specific post"""
    return [comment for comment in community_comments_db if comment.post_id == post_id]

@router.post("/comments/{comment_id}/like")
def like_community_comment(comment_id: int):
    """Like a community comment"""
    for index, comment in enumerate(community_comments_db):
        if comment.id == comment_id:
            community_comments_db[index].like_count += 1
            return {"message": "Community comment liked successfully"}
    raise HTTPException(status_code=404, detail="Community comment not found")

@router.post("/comments/{comment_id}/approve")
def approve_community_comment(comment_id: int):
    """Approve a community comment"""
    for index, comment in enumerate(community_comments_db):
        if comment.id == comment_id:
            community_comments_db[index].is_approved = True
            return {"message": "Community comment approved successfully"}
    raise HTTPException(status_code=404, detail="Community comment not found")

@router.post("/comments/{comment_id}/reject")
def reject_community_comment(comment_id: int):
    """Reject a community comment"""
    for index, comment in enumerate(community_comments_db):
        if comment.id == comment_id:
            community_comments_db[index].is_approved = False
            return {"message": "Community comment rejected successfully"}
    raise HTTPException(status_code=404, detail="Community comment not found")

# Community User endpoints
@router.get("/users", response_model=List[CommunityUser])
def list_community_users():
    """List all community users"""
    return community_users_db

@router.get("/users/{user_id}", response_model=CommunityUser)
def get_community_user(user_id: int):
    """Get a specific community user by ID"""
    for user in community_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Community user not found")

@router.post("/users", response_model=CommunityUser)
def create_community_user(user: CommunityUserCreate):
    """Create a new community user"""
    new_id = max([u.id for u in community_users_db]) + 1 if community_users_db else 1
    new_user = CommunityUser(
        id=new_id,
        created_at=datetime.now(),
        **user.dict()
    )
    community_users_db.append(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=CommunityUser)
def update_community_user(user_id: int, user_update: CommunityUserCreate):
    """Update an existing community user"""
    for index, user in enumerate(community_users_db):
        if user.id == user_id:
            updated_user = CommunityUser(
                id=user_id,
                created_at=user.created_at,
                updated_at=datetime.now(),
                **user_update.dict()
            )
            community_users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="Community user not found")

@router.delete("/users/{user_id}")
def delete_community_user(user_id: int):
    """Delete a community user"""
    for index, user in enumerate(community_users_db):
        if user.id == user_id:
            del community_users_db[index]
            return {"message": "Community user deleted successfully"}
    raise HTTPException(status_code=404, detail="Community user not found")

@router.post("/users/{user_id}/promote-expert")
def promote_user_to_expert(user_id: int):
    """Promote a user to expert status"""
    for index, user in enumerate(community_users_db):
        if user.id == user_id:
            community_users_db[index].is_expert = True
            return {"message": "User promoted to expert successfully"}
    raise HTTPException(status_code=404, detail="Community user not found")

@router.post("/users/{user_id}/promote-moderator")
def promote_user_to_moderator(user_id: int):
    """Promote a user to moderator status"""
    for index, user in enumerate(community_users_db):
        if user.id == user_id:
            community_users_db[index].is_moderator = True
            return {"message": "User promoted to moderator successfully"}
    raise HTTPException(status_code=404, detail="Community user not found")

@router.post("/users/{user_id}/update-reputation")
def update_user_reputation(user_id: int, points: int):
    """Update a user's reputation score"""
    for index, user in enumerate(community_users_db):
        if user.id == user_id:
            community_users_db[index].reputation_score += points
            return {"message": "User reputation updated successfully"}
    raise HTTPException(status_code=404, detail="Community user not found")

# Community Badge endpoints
@router.get("/badges", response_model=List[CommunityBadge])
def list_community_badges():
    """List all community badges"""
    return community_badges_db

@router.get("/badges/{badge_id}", response_model=CommunityBadge)
def get_community_badge(badge_id: int):
    """Get a specific community badge by ID"""
    for badge in community_badges_db:
        if badge.id == badge_id:
            return badge
    raise HTTPException(status_code=404, detail="Community badge not found")

@router.post("/badges", response_model=CommunityBadge)
def create_community_badge(badge: CommunityBadgeCreate):
    """Create a new community badge"""
    new_id = max([b.id for b in community_badges_db]) + 1 if community_badges_db else 1
    new_badge = CommunityBadge(
        id=new_id,
        created_at=datetime.now(),
        **badge.dict()
    )
    community_badges_db.append(new_badge)
    return new_badge

@router.put("/badges/{badge_id}", response_model=CommunityBadge)
def update_community_badge(badge_id: int, badge_update: CommunityBadgeCreate):
    """Update an existing community badge"""
    for index, badge in enumerate(community_badges_db):
        if badge.id == badge_id:
            updated_badge = CommunityBadge(
                id=badge_id,
                created_at=badge.created_at,
                **badge_update.dict()
            )
            community_badges_db[index] = updated_badge
            return updated_badge
    raise HTTPException(status_code=404, detail="Community badge not found")

@router.delete("/badges/{badge_id}")
def delete_community_badge(badge_id: int):
    """Delete a community badge"""
    for index, badge in enumerate(community_badges_db):
        if badge.id == badge_id:
            del community_badges_db[index]
            return {"message": "Community badge deleted successfully"}
    raise HTTPException(status_code=404, detail="Community badge not found")

# Configuration endpoints
@router.get("/config/post-types", response_model=List[str])
def get_community_post_type_options():
    """Get available community post type options"""
    return get_community_post_types()

@router.get("/config/post-statuses", response_model=List[str])
def get_community_post_status_options():
    """Get available community post status options"""
    return get_community_post_statuses()

@router.get("/config/reputation-threshold", response_model=int)
def get_reputation_threshold_for_expert():
    """Get reputation threshold for expert status"""
    return get_reputation_threshold_expert()