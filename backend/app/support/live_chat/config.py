import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_live_chat_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a live chat configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/live-chat-config/key/{key}"
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
            "chat_statuses": ["Pending", "Active", "Closed", "Transferred"],
            "chat_priorities": ["Low", "Medium", "High"],
            "default_priority": "Medium",
            "max_message_length": 1000
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "chat_statuses": ["Pending", "Active", "Closed", "Transferred"],
            "chat_priorities": ["Low", "Medium", "High"],
            "default_priority": "Medium",
            "max_message_length": 1000
        }
        
        return defaults.get(key, None)

def get_live_chat_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a live chat configuration value by key.
    
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
    return loop.run_until_complete(get_live_chat_config_from_superadmin(key, organization_id))

def get_chat_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available chat statuses"""
    return get_live_chat_config("chat_statuses", organization_id)

def get_chat_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available chat priorities"""
    return get_live_chat_config("chat_priorities", organization_id)

def get_default_priority(organization_id: Optional[int] = None) -> str:
    """Get default chat priority"""
    return get_live_chat_config("default_priority", organization_id)

def get_max_message_length(organization_id: Optional[int] = None) -> int:
    """Get maximum message length"""
    return get_live_chat_config("max_message_length", organization_id)