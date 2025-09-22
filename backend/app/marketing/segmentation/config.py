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
            "segment_types": ["Dynamic", "Static", "Account-Based"],
            "segment_criteria_types": ["Demographic", "Behavioral", "Firmographic", "Technographic", "Custom"],
            "default_member_count": 0,
            "default_target_count": 0,
            "max_criteria_per_segment": 20,
            "logical_operators": ["AND", "OR"]
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "segment_types": ["Dynamic", "Static", "Account-Based"],
            "segment_criteria_types": ["Demographic", "Behavioral", "Firmographic", "Technographic", "Custom"],
            "default_member_count": 0,
            "default_target_count": 0,
            "max_criteria_per_segment": 20,
            "logical_operators": ["AND", "OR"]
        }
        
        return defaults.get(key, None)

def get_segmentation_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a segmentation configuration value by key.
    
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

def get_segment_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available segment types"""
    return get_segmentation_config("segment_types", organization_id)

def get_segment_criteria_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available segment criteria types"""
    return get_segmentation_config("segment_criteria_types", organization_id)

def get_default_member_count(organization_id: Optional[int] = None) -> int:
    """Get default member count"""
    return get_segmentation_config("default_member_count", organization_id)

def get_default_target_count(organization_id: Optional[int] = None) -> int:
    """Get default target count"""
    return get_segmentation_config("default_target_count", organization_id)

def get_max_criteria_per_segment(organization_id: Optional[int] = None) -> int:
    """Get maximum criteria per segment"""
    return get_segmentation_config("max_criteria_per_segment", organization_id)

def get_logical_operators(organization_id: Optional[int] = None) -> List[str]:
    """Get available logical operators"""
    return get_segmentation_config("logical_operators", organization_id)