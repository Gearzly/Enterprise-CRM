import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_sales_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a sales configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/sales-config/key/{key}"
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
            "lead_statuses": ["New", "Contacted", "Qualified", "Unqualified", "Converted"],
            "lead_sources": ["Website", "Referral", "Social Media", "Email Campaign", "Event", "Other"],
            "opportunity_stages": ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
            "quotation_statuses": ["Draft", "Sent", "Viewed", "Accepted", "Rejected", "Expired"],
            "default_tax_rate": 0.0,
            "closed_won_stage": "Closed Won",
            "forecast_factors": ["Market growth", "New product launch", "Seasonal trends", "Economic conditions", "Competitor activity", "Historical trends"],
            "target_periods": ["Q1", "Q2", "Q3", "Q4", "H1", "H2", "Annual", "Monthly"]
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "lead_statuses": ["New", "Contacted", "Qualified", "Unqualified", "Converted"],
            "lead_sources": ["Website", "Referral", "Social Media", "Email Campaign", "Event", "Other"],
            "opportunity_stages": ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
            "quotation_statuses": ["Draft", "Sent", "Viewed", "Accepted", "Rejected", "Expired"],
            "default_tax_rate": 0.0,
            "closed_won_stage": "Closed Won",
            "forecast_factors": ["Market growth", "New product launch", "Seasonal trends", "Economic conditions", "Competitor activity", "Historical trends"],
            "target_periods": ["Q1", "Q2", "Q3", "Q4", "H1", "H2", "Annual", "Monthly"]
        }
        
        return defaults.get(key, None)

def get_sales_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a sales configuration value by key.
    
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
    return loop.run_until_complete(get_sales_config_from_superadmin(key, organization_id))

def get_lead_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead statuses"""
    return get_sales_config("lead_statuses", organization_id)

def get_lead_sources(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead sources"""
    return get_sales_config("lead_sources", organization_id)

def get_opportunity_stages(organization_id: Optional[int] = None) -> List[str]:
    """Get available opportunity stages"""
    return get_sales_config("opportunity_stages", organization_id)

def get_quotation_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available quotation statuses"""
    return get_sales_config("quotation_statuses", organization_id)

def get_default_tax_rate(organization_id: Optional[int] = None) -> float:
    """Get default tax rate"""
    return get_sales_config("default_tax_rate", organization_id)

def get_closed_won_stage(organization_id: Optional[int] = None) -> str:
    """Get the stage name for closed won opportunities"""
    return get_sales_config("closed_won_stage", organization_id)

def get_forecast_factors(organization_id: Optional[int] = None) -> List[str]:
    """Get available forecast factors"""
    return get_sales_config("forecast_factors", organization_id)

def get_target_periods(organization_id: Optional[int] = None) -> List[str]:
    """Get available target periods"""
    return get_sales_config("target_periods", organization_id)