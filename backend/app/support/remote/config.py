import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_remote_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a remote support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/remote-config/key/{key}"
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
            "remote_session_types": ["Desktop", "Mobile", "Server"],
            "remote_platforms": ["Windows", "macOS", "Linux", "Android", "iOS"],
            "remote_session_statuses": ["Pending", "Active", "Completed", "Failed", "Cancelled"],
            "default_session_type": "Desktop",
            "default_platform": "Windows",
            "max_file_transfer_size_mb": 100
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "remote_session_types": ["Desktop", "Mobile", "Server"],
            "remote_platforms": ["Windows", "macOS", "Linux", "Android", "iOS"],
            "remote_session_statuses": ["Pending", "Active", "Completed", "Failed", "Cancelled"],
            "default_session_type": "Desktop",
            "default_platform": "Windows",
            "max_file_transfer_size_mb": 100
        }
        
        return defaults.get(key, None)

def get_remote_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a remote support configuration value by key.
    
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
    return loop.run_until_complete(get_remote_config_from_superadmin(key, organization_id))

def get_remote_session_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available remote session types"""
    return get_remote_config("remote_session_types", organization_id)

def get_remote_platforms(organization_id: Optional[int] = None) -> List[str]:
    """Get available remote platforms"""
    return get_remote_config("remote_platforms", organization_id)

def get_remote_session_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available remote session statuses"""
    return get_remote_config("remote_session_statuses", organization_id)

def get_default_session_type(organization_id: Optional[int] = None) -> str:
    """Get default remote session type"""
    return get_remote_config("default_session_type", organization_id)

def get_default_platform(organization_id: Optional[int] = None) -> str:
    """Get default remote platform"""
    return get_remote_config("default_platform", organization_id)

def get_max_file_transfer_size_mb(organization_id: Optional[int] = None) -> int:
    """Get maximum file transfer size in MB"""
    return get_remote_config("max_file_transfer_size_mb", organization_id)