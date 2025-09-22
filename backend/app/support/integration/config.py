import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_integration_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an integration configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/integration-config/key/{key}"
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
            "integration_types": ["CRM", "E-commerce", "Productivity", "Custom"],
            "integration_platforms": ["Salesforce", "HubSpot", "Shopify", "WooCommerce", "Slack", "Microsoft Teams", "Custom"],
            "integration_statuses": ["Active", "Inactive", "Error", "Pending"],
            "default_integration_type": "CRM",
            "default_integration_platform": "Salesforce",
            "sync_frequency_minutes": 30
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "integration_types": ["CRM", "E-commerce", "Productivity", "Custom"],
            "integration_platforms": ["Salesforce", "HubSpot", "Shopify", "WooCommerce", "Slack", "Microsoft Teams", "Custom"],
            "integration_statuses": ["Active", "Inactive", "Error", "Pending"],
            "default_integration_type": "CRM",
            "default_integration_platform": "Salesforce",
            "sync_frequency_minutes": 30
        }
        
        return defaults.get(key, None)

def get_integration_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an integration configuration value by key.
    
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
    return loop.run_until_complete(get_integration_config_from_superadmin(key, organization_id))

def get_integration_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available integration types"""
    return get_integration_config("integration_types", organization_id)

def get_integration_platforms(organization_id: Optional[int] = None) -> List[str]:
    """Get available integration platforms"""
    return get_integration_config("integration_platforms", organization_id)

def get_integration_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available integration statuses"""
    return get_integration_config("integration_statuses", organization_id)

def get_default_integration_type(organization_id: Optional[int] = None) -> str:
    """Get default integration type"""
    return get_integration_config("default_integration_type", organization_id)

def get_default_integration_platform(organization_id: Optional[int] = None) -> str:
    """Get default integration platform"""
    return get_integration_config("default_integration_platform", organization_id)

def get_sync_frequency_minutes(organization_id: Optional[int] = None) -> int:
    """Get sync frequency in minutes"""
    return get_integration_config("sync_frequency_minutes", organization_id)