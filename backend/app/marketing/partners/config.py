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
            "partner_statuses": ["Active", "Inactive", "Pending", "Suspended"],
            "partner_types": [
                "Reseller",
                "Distributor",
                "Affiliate",
                "Technology Partner",
                "Strategic Partner",
                "Other"
            ],
            "default_commission_rate": 0.0,
            "default_conversion_rate": 0.0,
            "default_satisfaction_score": 0.0,
            "max_affiliate_commission": 0.5
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "partner_statuses": ["Active", "Inactive", "Pending", "Suspended"],
            "partner_types": [
                "Reseller",
                "Distributor",
                "Affiliate",
                "Technology Partner",
                "Strategic Partner",
                "Other"
            ],
            "default_commission_rate": 0.0,
            "default_conversion_rate": 0.0,
            "default_satisfaction_score": 0.0,
            "max_affiliate_commission": 0.5
        }
        
        return defaults.get(key, None)

def get_partner_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a partner configuration value by key.
    
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

def get_partner_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available partner statuses"""
    return get_partner_config("partner_statuses", organization_id)

def get_partner_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available partner types"""
    return get_partner_config("partner_types", organization_id)

def get_default_commission_rate(organization_id: Optional[int] = None) -> float:
    """Get default commission rate"""
    return get_partner_config("default_commission_rate", organization_id)

def get_default_conversion_rate(organization_id: Optional[int] = None) -> float:
    """Get default conversion rate"""
    return get_partner_config("default_conversion_rate", organization_id)

def get_default_satisfaction_score(organization_id: Optional[int] = None) -> float:
    """Get default satisfaction score"""
    return get_partner_config("default_satisfaction_score", organization_id)

def get_max_affiliate_commission(organization_id: Optional[int] = None) -> float:
    """Get maximum affiliate commission"""
    return get_partner_config("max_affiliate_commission", organization_id)