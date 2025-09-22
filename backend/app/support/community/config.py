import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_community_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a community support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/community-config/key/{key}"
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
            "community_post_types": ["Discussion", "Question", "Announcement", "Tutorial"],
            "community_post_statuses": ["Draft", "Published", "Archived", "Deleted"],
            "default_post_type": "Discussion",
            "default_post_status": "Published",
            "max_tags_per_post": 10,
            "reputation_threshold_expert": 1000
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "community_post_types": ["Discussion", "Question", "Announcement", "Tutorial"],
            "community_post_statuses": ["Draft", "Published", "Archived", "Deleted"],
            "default_post_type": "Discussion",
            "default_post_status": "Published",
            "max_tags_per_post": 10,
            "reputation_threshold_expert": 1000
        }
        
        return defaults.get(key, None)

def get_community_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a community support configuration value by key.
    
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
    return loop.run_until_complete(get_community_config_from_superadmin(key, organization_id))

def get_community_post_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available community post types"""
    return get_community_config("community_post_types", organization_id)

def get_community_post_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available community post statuses"""
    return get_community_config("community_post_statuses", organization_id)

def get_default_post_type(organization_id: Optional[int] = None) -> str:
    """Get default community post type"""
    return get_community_config("default_post_type", organization_id)

def get_default_post_status(organization_id: Optional[int] = None) -> str:
    """Get default community post status"""
    return get_community_config("default_post_status", organization_id)

def get_max_tags_per_post(organization_id: Optional[int] = None) -> int:
    """Get maximum number of tags per post"""
    return get_community_config("max_tags_per_post", organization_id)

def get_reputation_threshold_expert(organization_id: Optional[int] = None) -> int:
    """Get reputation threshold for expert status"""
    return get_community_config("reputation_threshold_expert", organization_id)