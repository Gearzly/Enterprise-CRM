import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_support_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/support-config/key/{key}"
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
            "ticket_priorities": ["Low", "Medium", "High", "Urgent"],
            "ticket_statuses": ["New", "In Progress", "Resolved", "Closed", "Reopened"],
            "ticket_channels": ["Email", "Web", "Phone", "Chat"],
            "default_priority": "Medium",
            "default_status": "New"
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "ticket_priorities": ["Low", "Medium", "High", "Urgent"],
            "ticket_statuses": ["New", "In Progress", "Resolved", "Closed", "Reopened"],
            "ticket_channels": ["Email", "Web", "Phone", "Chat"],
            "default_priority": "Medium",
            "default_status": "New"
        }
        
        return defaults.get(key, None)

def get_ticket_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a ticket configuration value by key.
    
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
    return loop.run_until_complete(get_support_config_from_superadmin(key, organization_id))

def get_ticket_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket priorities"""
    return get_ticket_config("ticket_priorities", organization_id)

def get_ticket_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket statuses"""
    return get_ticket_config("ticket_statuses", organization_id)

def get_ticket_channels(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket channels"""
    return get_ticket_config("ticket_channels", organization_id)

def get_default_priority(organization_id: Optional[int] = None) -> str:
    """Get default ticket priority"""
    return get_ticket_config("default_priority", organization_id)

def get_default_status(organization_id: Optional[int] = None) -> str:
    """Get default ticket status"""
    return get_ticket_config("default_status", organization_id)