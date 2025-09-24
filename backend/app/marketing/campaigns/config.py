import json
import httpx
from typing import List, Optional, Any
from app.core.config.dynamic_config import get_config_value

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
            "campaign_statuses": ["Draft", "Scheduled", "Active", "Paused", "Completed", "Cancelled"],
            "campaign_types": ["Email", "Social Media", "Direct Mail", "PPC", "Content", "Event", "Other"],
            "ab_test_metrics": ["click_rate", "conversion_rate", "open_rate", "bounce_rate"],
            "default_budget": 0.0
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "campaign_statuses": ["Draft", "Scheduled", "Active", "Paused", "Completed", "Cancelled"],
            "campaign_types": ["Email", "Social Media", "Direct Mail", "PPC", "Content", "Event", "Other"],
            "ab_test_metrics": ["click_rate", "conversion_rate", "open_rate", "bounce_rate"],
            "default_budget": 0.0
        }
        
        return defaults.get(key, None)

def get_campaign_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a campaign configuration value by key.
    
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

def get_campaign_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available campaign statuses"""
    value = get_config_value("marketing.campaign_statuses", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Draft", "Scheduled", "Active", "Paused", "Completed", "Cancelled"]

def get_campaign_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available campaign types"""
    value = get_config_value("marketing.campaign_types", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Email", "Social Media", "Direct Mail", "PPC", "Content", "Event", "Other"]

def get_ab_test_metrics(organization_id: Optional[int] = None) -> List[str]:
    """Get available A/B test metrics"""
    value = get_config_value("marketing.ab_test_metrics", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["click_rate", "conversion_rate", "open_rate", "bounce_rate"]

def get_default_budget(organization_id: Optional[int] = None) -> float:
    """Get default campaign budget"""
    value = get_config_value("marketing.default_budget", organization_id)
    # Ensure we return a float, even if the config returns None
    return float(value) if value is not None else 0.0
