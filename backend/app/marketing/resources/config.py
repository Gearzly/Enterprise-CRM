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
            "budget_statuses": ["Draft", "Approved", "Active", "Completed", "Cancelled"],
            "budget_categories": [
                "Campaigns",
                "Content",
                "Events",
                "Technology",
                "Personnel",
                "Agency Fees",
                "Other"
            ],
            "asset_types": ["Image", "Video", "Document", "Template", "Brand Asset", "Other"],
            "asset_statuses": ["Draft", "Review", "Approved", "Published", "Archived"],
            "default_utilization_percentage": 0.0,
            "max_file_size_mb": 100
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "budget_statuses": ["Draft", "Approved", "Active", "Completed", "Cancelled"],
            "budget_categories": [
                "Campaigns",
                "Content",
                "Events",
                "Technology",
                "Personnel",
                "Agency Fees",
                "Other"
            ],
            "asset_types": ["Image", "Video", "Document", "Template", "Brand Asset", "Other"],
            "asset_statuses": ["Draft", "Review", "Approved", "Published", "Archived"],
            "default_utilization_percentage": 0.0,
            "max_file_size_mb": 100
        }
        
        return defaults.get(key, None)

def get_resource_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a resource configuration value by key.
    
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

def get_budget_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available budget statuses"""
    return get_resource_config("budget_statuses", organization_id)

def get_budget_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available budget categories"""
    return get_resource_config("budget_categories", organization_id)

def get_asset_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available asset types"""
    return get_resource_config("asset_types", organization_id)

def get_asset_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available asset statuses"""
    return get_resource_config("asset_statuses", organization_id)

def get_default_utilization_percentage(organization_id: Optional[int] = None) -> float:
    """Get default utilization percentage"""
    return get_resource_config("default_utilization_percentage", organization_id)

def get_max_file_size_mb(organization_id: Optional[int] = None) -> int:
    """Get maximum file size in MB"""
    return get_resource_config("max_file_size_mb", organization_id)