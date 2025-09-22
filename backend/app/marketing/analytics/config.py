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
            "report_types": [
                "Campaign Performance",
                "Lead Generation",
                "Email Marketing",
                "Social Media",
                "Content Performance",
                "ROI Dashboard",
                "Conversion Tracking",
                "Attribution Modeling",
                "Customer Lifetime Value",
                "Channel Performance"
            ],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Custom"],
            "attribution_models": ["First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped", "W-Shaped"],
            "default_conversion_rate": 0.0,
            "default_customer_lifetime_value": 0.0,
            "max_dashboard_widgets": 20
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "report_types": [
                "Campaign Performance",
                "Lead Generation",
                "Email Marketing",
                "Social Media",
                "Content Performance",
                "ROI Dashboard",
                "Conversion Tracking",
                "Attribution Modeling",
                "Customer Lifetime Value",
                "Channel Performance"
            ],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Custom"],
            "attribution_models": ["First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped", "W-Shaped"],
            "default_conversion_rate": 0.0,
            "default_customer_lifetime_value": 0.0,
            "max_dashboard_widgets": 20
        }
        
        return defaults.get(key, None)

def get_analytics_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an analytics configuration value by key.
    
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

def get_report_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available report types"""
    return get_analytics_config("report_types", organization_id)

def get_report_frequencies(organization_id: Optional[int] = None) -> List[str]:
    """Get available report frequencies"""
    return get_analytics_config("report_frequencies", organization_id)

def get_attribution_models(organization_id: Optional[int] = None) -> List[str]:
    """Get available attribution models"""
    return get_analytics_config("attribution_models", organization_id)

def get_default_conversion_rate(organization_id: Optional[int] = None) -> float:
    """Get default conversion rate"""
    return get_analytics_config("default_conversion_rate", organization_id)

def get_default_customer_lifetime_value(organization_id: Optional[int] = None) -> float:
    """Get default customer lifetime value"""
    return get_analytics_config("default_customer_lifetime_value", organization_id)

def get_max_dashboard_widgets(organization_id: Optional[int] = None) -> int:
    """Get maximum dashboard widgets"""
    return get_analytics_config("max_dashboard_widgets", organization_id)