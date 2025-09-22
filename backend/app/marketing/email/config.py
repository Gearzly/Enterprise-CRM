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
            "email_statuses": ["Draft", "Scheduled", "Sending", "Sent", "Failed"],
            "email_template_categories": ["Newsletter", "Promotional", "Transactional", "Welcome", "Abandoned Cart", "Other"],
            "default_open_rate": 0.0,
            "default_click_rate": 0.0,
            "default_bounce_rate": 0.0,
            "max_email_size_kb": 1024,
            "daily_send_limit": 10000
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "email_statuses": ["Draft", "Scheduled", "Sending", "Sent", "Failed"],
            "email_template_categories": ["Newsletter", "Promotional", "Transactional", "Welcome", "Abandoned Cart", "Other"],
            "default_open_rate": 0.0,
            "default_click_rate": 0.0,
            "default_bounce_rate": 0.0,
            "max_email_size_kb": 1024,
            "daily_send_limit": 10000
        }
        
        return defaults.get(key, None)

def get_email_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an email configuration value by key.
    
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

def get_email_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available email statuses"""
    return get_email_config("email_statuses", organization_id)

def get_email_template_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available email template categories"""
    return get_email_config("email_template_categories", organization_id)

def get_default_open_rate(organization_id: Optional[int] = None) -> float:
    """Get default email open rate"""
    return get_email_config("default_open_rate", organization_id)

def get_default_click_rate(organization_id: Optional[int] = None) -> float:
    """Get default email click rate"""
    return get_email_config("default_click_rate", organization_id)

def get_default_bounce_rate(organization_id: Optional[int] = None) -> float:
    """Get default email bounce rate"""
    return get_email_config("default_bounce_rate", organization_id)

def get_max_email_size_kb(organization_id: Optional[int] = None) -> int:
    """Get maximum email size in KB"""
    return get_email_config("max_email_size_kb", organization_id)

def get_daily_send_limit(organization_id: Optional[int] = None) -> int:
    """Get daily email send limit"""
    return get_email_config("daily_send_limit", organization_id)