import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_sla_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an SLA configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/sla-config/key/{key}"
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
            "sla_types": ["Response", "Resolution", "First Response"],
            "default_sla_type": "Response",
            "default_response_time_hours": 24,
            "max_notification_threshold": 90
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "sla_types": ["Response", "Resolution", "First Response"],
            "default_sla_type": "Response",
            "default_response_time_hours": 24,
            "max_notification_threshold": 90
        }
        
        return defaults.get(key, None)

def get_sla_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an SLA configuration value by key.
    
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
    return loop.run_until_complete(get_sla_config_from_superadmin(key, organization_id))

def get_sla_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available SLA types"""
    return get_sla_config("sla_types", organization_id)

def get_default_sla_type(organization_id: Optional[int] = None) -> str:
    """Get default SLA type"""
    return get_sla_config("default_sla_type", organization_id)

def get_default_response_time_hours(organization_id: Optional[int] = None) -> int:
    """Get default response time in hours"""
    return get_sla_config("default_response_time_hours", organization_id)

def get_max_notification_threshold(organization_id: Optional[int] = None) -> int:
    """Get maximum notification threshold percentage"""
    return get_sla_config("max_notification_threshold", organization_id)