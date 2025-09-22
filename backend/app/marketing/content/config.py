import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_marketing_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a marketing configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/marketing-config/key/{key}"
            params = {"organization_id": organization_id} if organization_id else {}
            response = await client.get(url, params=params)
            response.raise_for_status()
            config = response.json()
            return json.loads(config["value"])
    except httpx.RequestError as e:
        # Log the error and return default values
        print(f"Error connecting to super admin API: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "content_statuses": ["Draft", "Review", "Approved", "Published", "Archived"],
            "content_types": ["Blog Post", "Video", "Image", "Infographic", "eBook", "Whitepaper", "Case Study", "Webinar", "Podcast", "Other"],
            "content_categories": ["Educational", "Promotional", "News", "Thought Leadership", "Customer Story", "Other"],
            "default_view_count": 0,
            "default_engagement_score": 0.0,
            "max_tags_per_content": 20,
            "max_seo_keywords": 10
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "content_statuses": ["Draft", "Review", "Approved", "Published", "Archived"],
            "content_types": ["Blog Post", "Video", "Image", "Infographic", "eBook", "Whitepaper", "Case Study", "Webinar", "Podcast", "Other"],
            "content_categories": ["Educational", "Promotional", "News", "Thought Leadership", "Customer Story", "Other"],
            "default_view_count": 0,
            "default_engagement_score": 0.0,
            "max_tags_per_content": 20,
            "max_seo_keywords": 10
        }
        
        return defaults.get(key, None)

def get_content_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a content configuration value by key.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    # This is a synchronous wrapper for the async function
    # In a real implementation, you would use the async function directly in FastAPI endpoints
    import asyncio
    try:
        # Try to get the running event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # If no event loop is running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the async function
    return loop.run_until_complete(get_marketing_config_from_superadmin(key, organization_id))

def get_content_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available content statuses"""
    return get_content_config("content_statuses", organization_id)

def get_content_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available content types"""
    return get_content_config("content_types", organization_id)

def get_content_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available content categories"""
    return get_content_config("content_categories", organization_id)

def get_default_view_count(organization_id: Optional[int] = None) -> int:
    """Get default view count"""
    return get_content_config("default_view_count", organization_id)

def get_default_engagement_score(organization_id: Optional[int] = None) -> float:
    """Get default engagement score"""
    return get_content_config("default_engagement_score", organization_id)

def get_max_tags_per_content(organization_id: Optional[int] = None) -> int:
    """Get maximum tags per content"""
    return get_content_config("max_tags_per_content", organization_id)

def get_max_seo_keywords(organization_id: Optional[int] = None) -> int:
    """Get maximum SEO keywords"""
    return get_content_config("max_seo_keywords", organization_id)