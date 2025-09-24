import json
import httpx
from typing import List, Any, Optional
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
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            config = response.json()
            return json.loads(config["value"])
    except httpx.RequestError as e:
        # Log the error and return default values
        print(f"Error connecting to super admin API: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "lead_statuses": ["New", "Contacted", "Nurtured", "Qualified", "Unqualified", "Converted"],
            "lead_sources": ["Website", "Referral", "Social Media", "Email Campaign", "Event", "Partner", "Other"],
            "lead_score_rule_types": ["Demographic", "Behavioral", "Engagement", "Firmographic"],
            "report_types": [
                "Campaign Performance", "Lead Generation", "Email Marketing", "Social Media",
                "Content Performance", "ROI Dashboard", "Conversion Tracking", "Attribution Modeling",
                "Customer Lifetime Value", "Channel Performance"
            ],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Custom"],
            "attribution_models": [
                "First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped", "W-Shaped"
            ],
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "lead_statuses": ["New", "Contacted", "Nurtured", "Qualified", "Unqualified", "Converted"],
            "lead_sources": ["Website", "Referral", "Social Media", "Email Campaign", "Event", "Partner", "Other"],
            "lead_score_rule_types": ["Demographic", "Behavioral", "Engagement", "Firmographic"],
            "report_types": [
                "Campaign Performance", "Lead Generation", "Email Marketing", "Social Media",
                "Content Performance", "ROI Dashboard", "Conversion Tracking", "Attribution Modeling",
                "Customer Lifetime Value", "Channel Performance"
            ],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Custom"],
            "attribution_models": [
                "First Touch", "Last Touch", "Linear", "Time Decay", "U-Shaped", "W-Shaped"
            ],
        }
        
        return defaults.get(key, None)

def get_marketing_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a marketing configuration value by key.
    
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

def get_lead_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead statuses"""
    return get_marketing_config("lead_statuses", organization_id)

def get_lead_sources(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead sources"""
    return get_marketing_config("lead_sources", organization_id)

def get_lead_score_rule_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead score rule types"""
    return get_marketing_config("lead_score_rule_types", organization_id)

def get_report_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available report types"""
    return get_marketing_config("report_types", organization_id)

def get_report_frequencies(organization_id: Optional[int] = None) -> List[str]:
    """Get available report frequencies"""
    return get_marketing_config("report_frequencies", organization_id)

def get_attribution_models(organization_id: Optional[int] = None) -> List[str]:
    """Get available attribution models"""
    return get_marketing_config("attribution_models", organization_id)