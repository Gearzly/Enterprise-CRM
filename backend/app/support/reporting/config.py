import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_reporting_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a reporting configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/reporting-config/key/{key}"
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
            "report_types": ["Ticket Metrics", "Agent Performance", "Customer Satisfaction", "Response Time", "Resolution Time", "SLA Compliance"],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"],
            "report_statuses": ["Pending", "Generating", "Completed", "Failed"],
            "default_report_frequency": "Weekly",
            "default_report_type": "Ticket Metrics",
            "max_data_points_per_report": 1000
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "report_types": ["Ticket Metrics", "Agent Performance", "Customer Satisfaction", "Response Time", "Resolution Time", "SLA Compliance"],
            "report_frequencies": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"],
            "report_statuses": ["Pending", "Generating", "Completed", "Failed"],
            "default_report_frequency": "Weekly",
            "default_report_type": "Ticket Metrics",
            "max_data_points_per_report": 1000
        }
        
        return defaults.get(key, None)

def get_reporting_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a reporting configuration value by key.
    
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
    return loop.run_until_complete(get_reporting_config_from_superadmin(key, organization_id))

def get_report_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available report types"""
    return get_reporting_config("report_types", organization_id)

def get_report_frequencies(organization_id: Optional[int] = None) -> List[str]:
    """Get available report frequencies"""
    return get_reporting_config("report_frequencies", organization_id)

def get_report_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available report statuses"""
    return get_reporting_config("report_statuses", organization_id)

def get_default_report_frequency(organization_id: Optional[int] = None) -> str:
    """Get default report frequency"""
    return get_reporting_config("default_report_frequency", organization_id)

def get_default_report_type(organization_id: Optional[int] = None) -> str:
    """Get default report type"""
    return get_reporting_config("default_report_type", organization_id)

def get_max_data_points_per_report(organization_id: Optional[int] = None) -> int:
    """Get maximum data points per report"""
    return get_reporting_config("max_data_points_per_report", organization_id)