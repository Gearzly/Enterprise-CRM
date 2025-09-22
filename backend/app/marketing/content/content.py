from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .models import (
    ContentAsset, ContentAssetCreate, ContentAssetUpdate,
    ContentPersonalization, ContentPersonalizationCreate, ContentPersonalizationUpdate,
    BlogPost, BlogPostCreate, BlogPostUpdate
)
from .config import (
    get_content_statuses, get_content_types, get_content_categories,
    get_default_view_count, get_default_engagement_score
)

router = APIRouter()

# In-memory storage for demo purposes
content_assets_db = []
content_personalizations_db = []
blog_posts_db = []

@router.get("/assets", response_model=List[ContentAsset])
def list_content_assets():
    """List all content assets"""
    return content_assets_db

@router.get("/assets/{asset_id}", response_model=ContentAsset)
def get_content_asset(asset_id: int):
    """Get a specific content asset by ID"""
    for asset in content_assets_db:
        if asset.id == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Content asset not found")

@router.post("/assets", response_model=ContentAsset)
def create_content_asset(asset: ContentAssetCreate):
    """Create a new content asset"""
    new_id = max([a.id for a in content_assets_db]) + 1 if content_assets_db else 1
    new_asset = ContentAsset(
        id=new_id,
        created_at=datetime.now(),
        view_count=get_default_view_count(),
        engagement_score=get_default_engagement_score(),
        **asset.dict()
    )
    content_assets_db.append(new_asset)
    return new_asset

@router.put("/assets/{asset_id}", response_model=ContentAsset)
def update_content_asset(asset_id: int, asset_update: ContentAssetUpdate):
    """Update an existing content asset"""
    for index, asset in enumerate(content_assets_db):
        if asset.id == asset_id:
            updated_asset = ContentAsset(
                id=asset_id,
                created_at=asset.created_at,
                updated_at=datetime.now(),
                view_count=asset.view_count,
                download_count=asset.download_count,
                engagement_score=asset.engagement_score,
                **asset_update.dict()
            )
            content_assets_db[index] = updated_asset
            return updated_asset
    raise HTTPException(status_code=404, detail="Content asset not found")

@router.delete("/assets/{asset_id}")
def delete_content_asset(asset_id: int):
    """Delete a content asset"""
    for index, asset in enumerate(content_assets_db):
        if asset.id == asset_id:
            del content_assets_db[index]
            return {"message": "Content asset deleted successfully"}
    raise HTTPException(status_code=404, detail="Content asset not found")

@router.get("/assets/status/{status}", response_model=List[ContentAsset])
def get_content_assets_by_status(status: str):
    """Get content assets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [asset for asset in content_assets_db if asset.status.value == normalized_status]

@router.get("/assets/type/{content_type}", response_model=List[ContentAsset])
def get_content_assets_by_type(content_type: str):
    """Get content assets by type"""
    # Normalize the content_type parameter to handle case differences
    normalized_type = content_type.lower().title()
    return [asset for asset in content_assets_db if asset.content_type.value == normalized_type]

@router.get("/assets/category/{category}", response_model=List[ContentAsset])
def get_content_assets_by_category(category: str):
    """Get content assets by category"""
    # Normalize the category parameter to handle case differences
    normalized_category = category.lower().title()
    return [asset for asset in content_assets_db if asset.category.value == normalized_category]

# Content Personalization endpoints
@router.get("/personalizations", response_model=List[ContentPersonalization])
def list_content_personalizations():
    """List all content personalizations"""
    return content_personalizations_db

@router.get("/personalizations/{personalization_id}", response_model=ContentPersonalization)
def get_content_personalization(personalization_id: int):
    """Get a specific content personalization by ID"""
    for personalization in content_personalizations_db:
        if personalization.id == personalization_id:
            return personalization
    raise HTTPException(status_code=404, detail="Content personalization not found")

@router.post("/personalizations", response_model=ContentPersonalization)
def create_content_personalization(personalization: ContentPersonalizationCreate):
    """Create a new content personalization"""
    new_id = max([p.id for p in content_personalizations_db]) + 1 if content_personalizations_db else 1
    new_personalization = ContentPersonalization(
        id=new_id,
        created_at=datetime.now(),
        **personalization.dict()
    )
    content_personalizations_db.append(new_personalization)
    return new_personalization

@router.put("/personalizations/{personalization_id}", response_model=ContentPersonalization)
def update_content_personalization(personalization_id: int, personalization_update: ContentPersonalizationUpdate):
    """Update an existing content personalization"""
    for index, personalization in enumerate(content_personalizations_db):
        if personalization.id == personalization_id:
            updated_personalization = ContentPersonalization(
                id=personalization_id,
                created_at=personalization.created_at,
                updated_at=datetime.now(),
                **personalization_update.dict()
            )
            content_personalizations_db[index] = updated_personalization
            return updated_personalization
    raise HTTPException(status_code=404, detail="Content personalization not found")

@router.delete("/personalizations/{personalization_id}")
def delete_content_personalization(personalization_id: int):
    """Delete a content personalization"""
    for index, personalization in enumerate(content_personalizations_db):
        if personalization.id == personalization_id:
            del content_personalizations_db[index]
            return {"message": "Content personalization deleted successfully"}
    raise HTTPException(status_code=404, detail="Content personalization not found")

# Blog Posts endpoints
@router.get("/blog-posts", response_model=List[BlogPost])
def list_blog_posts():
    """List all blog posts"""
    return blog_posts_db

@router.get("/blog-posts/{post_id}", response_model=BlogPost)
def get_blog_post(post_id: int):
    """Get a specific blog post by ID"""
    for post in blog_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Blog post not found")

@router.post("/blog-posts", response_model=BlogPost)
def create_blog_post(post: BlogPostCreate):
    """Create a new blog post"""
    new_id = max([p.id for p in blog_posts_db]) + 1 if blog_posts_db else 1
    new_post = BlogPost(
        id=new_id,
        created_at=datetime.now(),
        view_count=get_default_view_count(),
        **post.dict()
    )
    blog_posts_db.append(new_post)
    return new_post

@router.put("/blog-posts/{post_id}", response_model=BlogPost)
def update_blog_post(post_id: int, post_update: BlogPostUpdate):
    """Update an existing blog post"""
    for index, post in enumerate(blog_posts_db):
        if post.id == post_id:
            updated_post = BlogPost(
                id=post_id,
                created_at=post.created_at,
                updated_at=datetime.now(),
                view_count=post.view_count,
                comment_count=post.comment_count,
                like_count=post.like_count,
                **post_update.dict()
            )
            blog_posts_db[index] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Blog post not found")

@router.delete("/blog-posts/{post_id}")
def delete_blog_post(post_id: int):
    """Delete a blog post"""
    for index, post in enumerate(blog_posts_db):
        if post.id == post_id:
            del blog_posts_db[index]
            return {"message": "Blog post deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog post not found")

@router.post("/blog-posts/{post_id}/publish")
def publish_blog_post(post_id: int):
    """Publish a blog post"""
    for index, post in enumerate(blog_posts_db):
        if post.id == post_id:
            post.status = "Published"
            post.published_at = datetime.now()
            blog_posts_db[index] = post
            return {"message": f"Blog post {post_id} published successfully"}
    raise HTTPException(status_code=404, detail="Blog post not found")

@router.get("/blog-posts/status/{status}", response_model=List[BlogPost])
def get_blog_posts_by_status(status: str):
    """Get blog posts by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [post for post in blog_posts_db if post.status.value == normalized_status]

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_content_status_options():
    """Get available content statuses"""
    return get_content_statuses()

@router.get("/config/types", response_model=List[str])
def get_content_type_options():
    """Get available content types"""
    return get_content_types()

@router.get("/config/categories", response_model=List[str])
def get_content_category_options():
    """Get available content categories"""
    return get_content_categories()