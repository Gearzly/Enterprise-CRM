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
            "event_statuses": [
                "Draft",
                "Planned",
                "Registration Open",
                "Upcoming",
                "Ongoing",
                "Completed",
                "Cancelled"
            ],
            "event_types": [
                "Webinar",
                "Conference",
                "Trade Show",
                "Workshop",
                "Networking Event",
                "Product Launch",
                "Virtual Event",
                "Other"
            ],
            "default_registered_count": 0,
            "default_attended_count": 0,
            "default_capacity": 100,
            "max_event_tags": 10
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "event_statuses": [
                "Draft",
                "Planned",
                "Registration Open",
                "Upcoming",
                "Ongoing",
                "Completed",
                "Cancelled"
            ],
            "event_types": [
                "Webinar",
                "Conference",
                "Trade Show",
                "Workshop",
                "Networking Event",
                "Product Launch",
                "Virtual Event",
                "Other"
            ],
            "default_registered_count": 0,
            "default_attended_count": 0,
            "default_capacity": 100,
            "max_event_tags": 10
        }
        
        return defaults.get(key, None)

def get_event_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an event configuration value by key.
    
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

def get_event_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available event statuses"""
    return get_event_config("event_statuses", organization_id)

def get_event_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available event types"""
    return get_event_config("event_types", organization_id)

def get_default_registered_count(organization_id: Optional[int] = None) -> int:
    """Get default registered count"""
    return get_event_config("default_registered_count", organization_id)

def get_default_attended_count(organization_id: Optional[int] = None) -> int:
    """Get default attended count"""
    return get_event_config("default_attended_count", organization_id)

def get_default_capacity(organization_id: Optional[int] = None) -> int:
    """Get default event capacity"""
    return get_event_config("default_capacity", organization_id)

def get_max_event_tags(organization_id: Optional[int] = None) -> int:
    """Get maximum event tags"""
    return get_event_config("max_event_tags", organization_id)