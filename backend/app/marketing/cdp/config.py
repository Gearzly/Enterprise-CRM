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
            "data_source_types": [
                "CRM",
                "Website",
                "Email",
                "Social Media",
                "Mobile App",
                "Offline",
                "Third Party",
                "Other"
            ],
            "identity_resolution_statuses": ["Pending", "Matched", "Merged", "Conflicted"],
            "data_privacy_statuses": ["Compliant", "Pending Consent", "Restricted", "Deleted"],
            "default_profile_score": 0,
            "default_engagement_score": 0,
            "default_completeness_score": 0.0,
            "default_accuracy_score": 0.0,
            "sync_frequencies": ["hourly", "daily", "weekly", "monthly"]
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "data_source_types": [
                "CRM",
                "Website",
                "Email",
                "Social Media",
                "Mobile App",
                "Offline",
                "Third Party",
                "Other"
            ],
            "identity_resolution_statuses": ["Pending", "Matched", "Merged", "Conflicted"],
            "data_privacy_statuses": ["Compliant", "Pending Consent", "Restricted", "Deleted"],
            "default_profile_score": 0,
            "default_engagement_score": 0,
            "default_completeness_score": 0.0,
            "default_accuracy_score": 0.0,
            "sync_frequencies": ["hourly", "daily", "weekly", "monthly"]
        }
        
        return defaults.get(key, None)

def get_cdp_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a CDP configuration value by key.
    
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

def get_data_source_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available data source types"""
    return get_cdp_config("data_source_types", organization_id)

def get_identity_resolution_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available identity resolution statuses"""
    return get_cdp_config("identity_resolution_statuses", organization_id)

def get_data_privacy_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available data privacy statuses"""
    return get_cdp_config("data_privacy_statuses", organization_id)

def get_default_profile_score(organization_id: Optional[int] = None) -> int:
    """Get default profile score"""
    return get_cdp_config("default_profile_score", organization_id)

def get_default_engagement_score(organization_id: Optional[int] = None) -> int:
    """Get default engagement score"""
    return get_cdp_config("default_engagement_score", organization_id)

def get_default_completeness_score(organization_id: Optional[int] = None) -> float:
    """Get default completeness score"""
    return get_cdp_config("default_completeness_score", organization_id)

def get_default_accuracy_score(organization_id: Optional[int] = None) -> float:
    """Get default accuracy score"""
    return get_cdp_config("default_accuracy_score", organization_id)

def get_sync_frequencies(organization_id: Optional[int] = None) -> List[str]:
    """Get available sync frequencies"""
    return get_cdp_config("sync_frequencies", organization_id)