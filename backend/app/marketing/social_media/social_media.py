from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .models import (
    SocialPost, SocialPostCreate, SocialPostUpdate,
    SocialListeningKeyword, SocialListeningKeywordCreate, SocialListeningKeywordUpdate,
    SocialMention, SocialMentionCreate, SocialMentionUpdate,
    SocialEngagement, SocialEngagementCreate, SocialEngagementUpdate,
    Influencer, InfluencerCreate, InfluencerUpdate
)
from .config import (
    get_social_platforms, get_post_statuses, get_engagement_types,
    get_default_engagement_count
)

router = APIRouter()

# In-memory storage for demo purposes
social_posts_db = []
social_keywords_db = []
social_mentions_db = []
social_engagements_db = []
influencers_db = []

@router.get("/posts", response_model=List[SocialPost])
def list_social_posts():
    """List all social media posts"""
    return social_posts_db

@router.get("/posts/{post_id}", response_model=SocialPost)
def get_social_post(post_id: int):
    """Get a specific social media post by ID"""
    for post in social_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Social post not found")

@router.post("/posts", response_model=SocialPost)
def create_social_post(post: SocialPostCreate):
    """Create a new social media post"""
    new_id = max([p.id for p in social_posts_db]) + 1 if social_posts_db else 1
    new_post = SocialPost(
        id=new_id,
        created_at=datetime.now(),
        engagement_count=get_default_engagement_count(),
        **post.dict()
    )
    social_posts_db.append(new_post)
    return new_post

@router.put("/posts/{post_id}", response_model=SocialPost)
def update_social_post(post_id: int, post_update: SocialPostUpdate):
    """Update an existing social media post"""
    for index, post in enumerate(social_posts_db):
        if post.id == post_id:
            updated_post = SocialPost(
                id=post_id,
                created_at=post.created_at,
                updated_at=datetime.now(),
                engagement_count=post.engagement_count,
                like_count=post.like_count,
                share_count=post.share_count,
                comment_count=post.comment_count,
                view_count=post.view_count,
                **post_update.dict()
            )
            social_posts_db[index] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Social post not found")

@router.delete("/posts/{post_id}")
def delete_social_post(post_id: int):
    """Delete a social media post"""
    for index, post in enumerate(social_posts_db):
        if post.id == post_id:
            del social_posts_db[index]
            return {"message": "Social post deleted successfully"}
    raise HTTPException(status_code=404, detail="Social post not found")

@router.get("/posts/status/{status}", response_model=List[SocialPost])
def get_social_posts_by_status(status: str):
    """Get social posts by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [post for post in social_posts_db if post.status.value == normalized_status]

@router.get("/posts/platform/{platform}", response_model=List[SocialPost])
def get_social_posts_by_platform(platform: str):
    """Get social posts by platform"""
    # Normalize the platform parameter to handle case differences
    normalized_platform = platform.lower().title()
    return [post for post in social_posts_db if post.platform.value == normalized_platform]

@router.post("/posts/{post_id}/publish")
def publish_social_post(post_id: int):
    """Publish a social media post"""
    for index, post in enumerate(social_posts_db):
        if post.id == post_id:
            post.status = "Published"
            post.published_at = datetime.now()
            social_posts_db[index] = post
            return {"message": f"Social post {post_id} published successfully"}
    raise HTTPException(status_code=404, detail="Social post not found")

# Social Listening Keywords endpoints
@router.get("/keywords", response_model=List[SocialListeningKeyword])
def list_social_keywords():
    """List all social listening keywords"""
    return social_keywords_db

@router.get("/keywords/{keyword_id}", response_model=SocialListeningKeyword)
def get_social_keyword(keyword_id: int):
    """Get a specific social listening keyword by ID"""
    for keyword in social_keywords_db:
        if keyword.id == keyword_id:
            return keyword
    raise HTTPException(status_code=404, detail="Social listening keyword not found")

@router.post("/keywords", response_model=SocialListeningKeyword)
def create_social_keyword(keyword: SocialListeningKeywordCreate):
    """Create a new social listening keyword"""
    new_id = max([k.id for k in social_keywords_db]) + 1 if social_keywords_db else 1
    new_keyword = SocialListeningKeyword(
        id=new_id,
        created_at=datetime.now(),
        **keyword.dict()
    )
    social_keywords_db.append(new_keyword)
    return new_keyword

@router.put("/keywords/{keyword_id}", response_model=SocialListeningKeyword)
def update_social_keyword(keyword_id: int, keyword_update: SocialListeningKeywordUpdate):
    """Update an existing social listening keyword"""
    for index, keyword in enumerate(social_keywords_db):
        if keyword.id == keyword_id:
            updated_keyword = SocialListeningKeyword(
                id=keyword_id,
                created_at=keyword.created_at,
                updated_at=datetime.now(),
                mention_count=keyword.mention_count,
                **keyword_update.dict()
            )
            social_keywords_db[index] = updated_keyword
            return updated_keyword
    raise HTTPException(status_code=404, detail="Social listening keyword not found")

@router.delete("/keywords/{keyword_id}")
def delete_social_keyword(keyword_id: int):
    """Delete a social listening keyword"""
    for index, keyword in enumerate(social_keywords_db):
        if keyword.id == keyword_id:
            del social_keywords_db[index]
            return {"message": "Social listening keyword deleted successfully"}
    raise HTTPException(status_code=404, detail="Social listening keyword not found")

# Social Mentions endpoints
@router.get("/mentions", response_model=List[SocialMention])
def list_social_mentions():
    """List all social mentions"""
    return social_mentions_db

@router.get("/mentions/{mention_id}", response_model=SocialMention)
def get_social_mention(mention_id: int):
    """Get a specific social mention by ID"""
    for mention in social_mentions_db:
        if mention.id == mention_id:
            return mention
    raise HTTPException(status_code=404, detail="Social mention not found")

@router.post("/mentions", response_model=SocialMention)
def create_social_mention(mention: SocialMentionCreate):
    """Create a new social mention"""
    new_id = max([m.id for m in social_mentions_db]) + 1 if social_mentions_db else 1
    new_mention = SocialMention(
        id=new_id,
        created_at=datetime.now(),
        **mention.dict()
    )
    social_mentions_db.append(new_mention)
    return new_mention

@router.put("/mentions/{mention_id}", response_model=SocialMention)
def update_social_mention(mention_id: int, mention_update: SocialMentionUpdate):
    """Update an existing social mention"""
    for index, mention in enumerate(social_mentions_db):
        if mention.id == mention_id:
            updated_mention = SocialMention(
                id=mention_id,
                created_at=mention.created_at,
                updated_at=datetime.now(),
                **mention_update.dict()
            )
            social_mentions_db[index] = updated_mention
            return updated_mention
    raise HTTPException(status_code=404, detail="Social mention not found")

@router.delete("/mentions/{mention_id}")
def delete_social_mention(mention_id: int):
    """Delete a social mention"""
    for index, mention in enumerate(social_mentions_db):
        if mention.id == mention_id:
            del social_mentions_db[index]
            return {"message": "Social mention deleted successfully"}
    raise HTTPException(status_code=404, detail="Social mention not found")

@router.post("/mentions/{mention_id}/respond")
def respond_to_social_mention(mention_id: int):
    """Mark a social mention as responded"""
    for index, mention in enumerate(social_mentions_db):
        if mention.id == mention_id:
            mention.is_responded = True
            social_mentions_db[index] = mention
            return {"message": f"Social mention {mention_id} marked as responded"}
    raise HTTPException(status_code=404, detail="Social mention not found")

# Social Engagements endpoints
@router.get("/engagements", response_model=List[SocialEngagement])
def list_social_engagements():
    """List all social engagements"""
    return social_engagements_db

@router.get("/engagements/{engagement_id}", response_model=SocialEngagement)
def get_social_engagement(engagement_id: int):
    """Get a specific social engagement by ID"""
    for engagement in social_engagements_db:
        if engagement.id == engagement_id:
            return engagement
    raise HTTPException(status_code=404, detail="Social engagement not found")

@router.post("/engagements", response_model=SocialEngagement)
def create_social_engagement(engagement: SocialEngagementCreate):
    """Create a new social engagement"""
    new_id = max([e.id for e in social_engagements_db]) + 1 if social_engagements_db else 1
    new_engagement = SocialEngagement(
        id=new_id,
        **engagement.dict()
    )
    social_engagements_db.append(new_engagement)
    return new_engagement

@router.put("/engagements/{engagement_id}", response_model=SocialEngagement)
def update_social_engagement(engagement_id: int, engagement_update: SocialEngagementUpdate):
    """Update an existing social engagement"""
    for index, engagement in enumerate(social_engagements_db):
        if engagement.id == engagement_id:
            updated_engagement = SocialEngagement(
                id=engagement_id,
                **engagement_update.dict()
            )
            social_engagements_db[index] = updated_engagement
            return updated_engagement
    raise HTTPException(status_code=404, detail="Social engagement not found")

@router.delete("/engagements/{engagement_id}")
def delete_social_engagement(engagement_id: int):
    """Delete a social engagement"""
    for index, engagement in enumerate(social_engagements_db):
        if engagement.id == engagement_id:
            del social_engagements_db[index]
            return {"message": "Social engagement deleted successfully"}
    raise HTTPException(status_code=404, detail="Social engagement not found")

# Influencers endpoints
@router.get("/influencers", response_model=List[Influencer])
def list_influencers():
    """List all influencers"""
    return influencers_db

@router.get("/influencers/{influencer_id}", response_model=Influencer)
def get_influencer(influencer_id: int):
    """Get a specific influencer by ID"""
    for influencer in influencers_db:
        if influencer.id == influencer_id:
            return influencer
    raise HTTPException(status_code=404, detail="Influencer not found")

@router.post("/influencers", response_model=Influencer)
def create_influencer(influencer: InfluencerCreate):
    """Create a new influencer"""
    new_id = max([i.id for i in influencers_db]) + 1 if influencers_db else 1
    new_influencer = Influencer(
        id=new_id,
        created_at=datetime.now(),
        **influencer.dict()
    )
    influencers_db.append(new_influencer)
    return new_influencer

@router.put("/influencers/{influencer_id}", response_model=Influencer)
def update_influencer(influencer_id: int, influencer_update: InfluencerUpdate):
    """Update an existing influencer"""
    for index, influencer in enumerate(influencers_db):
        if influencer.id == influencer_id:
            updated_influencer = Influencer(
                id=influencer_id,
                created_at=influencer.created_at,
                updated_at=datetime.now(),
                **influencer_update.dict()
            )
            influencers_db[index] = updated_influencer
            return updated_influencer
    raise HTTPException(status_code=404, detail="Influencer not found")

@router.delete("/influencers/{influencer_id}")
def delete_influencer(influencer_id: int):
    """Delete an influencer"""
    for index, influencer in enumerate(influencers_db):
        if influencer.id == influencer_id:
            del influencers_db[index]
            return {"message": "Influencer deleted successfully"}
    raise HTTPException(status_code=404, detail="Influencer not found")

# Configuration endpoints
@router.get("/config/platforms", response_model=List[str])
def get_social_platform_options():
    """Get available social platforms"""
    return get_social_platforms()

@router.get("/config/post-statuses", response_model=List[str])
def get_post_status_options():
    """Get available post statuses"""
    return get_post_statuses()

@router.get("/config/engagement-types", response_model=List[str])
def get_engagement_type_options():
    """Get available engagement types"""
    return get_engagement_types()