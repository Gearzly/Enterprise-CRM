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
            "social_platforms": ["Facebook", "Twitter", "LinkedIn", "Instagram", "YouTube", "TikTok", "Pinterest", "Other"],
            "post_statuses": ["Draft", "Scheduled", "Published", "Failed"],
            "engagement_types": ["Like", "Share", "Comment", "View", "Click"],
            "default_engagement_count": 0,
            "max_media_per_post": 10,
            "max_post_length": 280
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "social_platforms": ["Facebook", "Twitter", "LinkedIn", "Instagram", "YouTube", "TikTok", "Pinterest", "Other"],
            "post_statuses": ["Draft", "Scheduled", "Published", "Failed"],
            "engagement_types": ["Like", "Share", "Comment", "View", "Click"],
            "default_engagement_count": 0,
            "max_media_per_post": 10,
            "max_post_length": 280
        }
        
        return defaults.get(key, None)

def get_social_media_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a social media configuration value by key.
    
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

def get_social_platforms(organization_id: Optional[int] = None) -> List[str]:
    """Get available social platforms"""
    return get_social_media_config("social_platforms", organization_id)

def get_post_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available post statuses"""
    return get_social_media_config("post_statuses", organization_id)

def get_engagement_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available engagement types"""
    return get_social_media_config("engagement_types", organization_id)

def get_default_engagement_count(organization_id: Optional[int] = None) -> int:
    """Get default engagement count"""
    return get_social_media_config("default_engagement_count", organization_id)

def get_max_media_per_post(organization_id: Optional[int] = None) -> int:
    """Get maximum media items per post"""
    return get_social_media_config("max_media_per_post", organization_id)

def get_max_post_length(organization_id: Optional[int] = None) -> int:
    """Get maximum post length"""
    return get_social_media_config("max_post_length", organization_id)