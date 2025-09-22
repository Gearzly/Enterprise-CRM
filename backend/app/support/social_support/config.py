import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_social_support_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a social support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/social-support-config/key/{key}"
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
            "social_platforms": ["Facebook", "Twitter", "Instagram", "LinkedIn", "YouTube", "TikTok"],
            "social_sentiments": ["Positive", "Neutral", "Negative"],
            "default_sentiment": "Neutral",
            "max_tags_per_inquiry": 5
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "social_platforms": ["Facebook", "Twitter", "Instagram", "LinkedIn", "YouTube", "TikTok"],
            "social_sentiments": ["Positive", "Neutral", "Negative"],
            "default_sentiment": "Neutral",
            "max_tags_per_inquiry": 5
        }
        
        return defaults.get(key, None)

def get_social_support_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a social support configuration value by key.
    
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
    return loop.run_until_complete(get_social_support_config_from_superadmin(key, organization_id))

def get_social_platforms(organization_id: Optional[int] = None) -> List[str]:
    """Get available social platforms"""
    return get_social_support_config("social_platforms", organization_id)

def get_social_sentiments(organization_id: Optional[int] = None) -> List[str]:
    """Get available social sentiments"""
    return get_social_support_config("social_sentiments", organization_id)

def get_default_sentiment(organization_id: Optional[int] = None) -> str:
    """Get default social sentiment"""
    return get_social_support_config("default_sentiment", organization_id)

def get_max_tags_per_inquiry(organization_id: Optional[int] = None) -> int:
    """Get maximum number of tags per inquiry"""
    return get_social_support_config("max_tags_per_inquiry", organization_id)