import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_feedback_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a feedback configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/feedback-config/key/{key}"
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
            "feedback_types": ["Survey", "NPS", "General", "Feature Request", "Bug Report"],
            "feedback_categories": ["Product", "Service", "Support", "Billing", "Other"],
            "feedback_statuses": ["Pending", "Reviewed", "Addressed", "Archived"],
            "default_category": "Other",
            "default_status": "Pending",
            "max_tags_per_feedback": 5
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "feedback_types": ["Survey", "NPS", "General", "Feature Request", "Bug Report"],
            "feedback_categories": ["Product", "Service", "Support", "Billing", "Other"],
            "feedback_statuses": ["Pending", "Reviewed", "Addressed", "Archived"],
            "default_category": "Other",
            "default_status": "Pending",
            "max_tags_per_feedback": 5
        }
        
        return defaults.get(key, None)

def get_feedback_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a feedback configuration value by key.
    
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
    return loop.run_until_complete(get_feedback_config_from_superadmin(key, organization_id))

def get_feedback_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available feedback types"""
    return get_feedback_config("feedback_types", organization_id)

def get_feedback_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available feedback categories"""
    return get_feedback_config("feedback_categories", organization_id)

def get_feedback_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available feedback statuses"""
    return get_feedback_config("feedback_statuses", organization_id)

def get_default_category(organization_id: Optional[int] = None) -> str:
    """Get default feedback category"""
    return get_feedback_config("default_category", organization_id)

def get_default_status(organization_id: Optional[int] = None) -> str:
    """Get default feedback status"""
    return get_feedback_config("default_status", organization_id)

def get_max_tags_per_feedback(organization_id: Optional[int] = None) -> int:
    """Get maximum number of tags per feedback"""
    return get_feedback_config("max_tags_per_feedback", organization_id)