import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_asset_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an asset configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/asset-config/key/{key}"
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
            "asset_types": ["Hardware", "Software", "Service", "Other"],
            "asset_statuses": ["Active", "Inactive", "Retired", "Broken"],
            "warranty_statuses": ["Active", "Expired", "Void"],
            "default_asset_type": "Hardware",
            "default_asset_status": "Active",
            "maintenance_reminder_days": 7
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "asset_types": ["Hardware", "Software", "Service", "Other"],
            "asset_statuses": ["Active", "Inactive", "Retired", "Broken"],
            "warranty_statuses": ["Active", "Expired", "Void"],
            "default_asset_type": "Hardware",
            "default_asset_status": "Active",
            "maintenance_reminder_days": 7
        }
        
        return defaults.get(key, None)

def get_asset_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an asset configuration value by key.
    
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
    return loop.run_until_complete(get_asset_config_from_superadmin(key, organization_id))

def get_asset_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available asset types"""
    return get_asset_config("asset_types", organization_id)

def get_asset_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available asset statuses"""
    return get_asset_config("asset_statuses", organization_id)

def get_warranty_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available warranty statuses"""
    return get_asset_config("warranty_statuses", organization_id)

def get_default_asset_type(organization_id: Optional[int] = None) -> str:
    """Get default asset type"""
    return get_asset_config("default_asset_type", organization_id)

def get_default_asset_status(organization_id: Optional[int] = None) -> str:
    """Get default asset status"""
    return get_asset_config("default_asset_status", organization_id)

def get_maintenance_reminder_days(organization_id: Optional[int] = None) -> int:
    """Get maintenance reminder days"""
    return get_asset_config("maintenance_reminder_days", organization_id)