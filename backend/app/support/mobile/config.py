import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_mobile_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a mobile support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/mobile-config/key/{key}"
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
            "mobile_device_types": ["iOS", "Android", "Windows Phone"],
            "mobile_app_types": ["Customer", "Agent"],
            "mobile_ticket_statuses": ["Offline Created", "Synced", "Pending Sync"],
            "default_device_type": "Android",
            "default_app_type": "Customer",
            "max_attachment_size_mb": 10
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "mobile_device_types": ["iOS", "Android", "Windows Phone"],
            "mobile_app_types": ["Customer", "Agent"],
            "mobile_ticket_statuses": ["Offline Created", "Synced", "Pending Sync"],
            "default_device_type": "Android",
            "default_app_type": "Customer",
            "max_attachment_size_mb": 10
        }
        
        return defaults.get(key, None)

def get_mobile_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a mobile support configuration value by key.
    
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
    return loop.run_until_complete(get_mobile_config_from_superadmin(key, organization_id))

def get_mobile_device_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available mobile device types"""
    return get_mobile_config("mobile_device_types", organization_id)

def get_mobile_app_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available mobile app types"""
    return get_mobile_config("mobile_app_types", organization_id)

def get_mobile_ticket_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available mobile ticket statuses"""
    return get_mobile_config("mobile_ticket_statuses", organization_id)

def get_default_device_type(organization_id: Optional[int] = None) -> str:
    """Get default mobile device type"""
    return get_mobile_config("default_device_type", organization_id)

def get_default_app_type(organization_id: Optional[int] = None) -> str:
    """Get default mobile app type"""
    return get_mobile_config("default_app_type", organization_id)

def get_max_attachment_size_mb(organization_id: Optional[int] = None) -> int:
    """Get maximum attachment size in MB"""
    return get_mobile_config("max_attachment_size_mb", organization_id)