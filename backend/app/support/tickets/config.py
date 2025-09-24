import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configuration cache to reduce API calls
_config_cache = {}

async def get_support_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a support configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    # Create a cache key
    cache_key = f"{key}:{organization_id}" if organization_id else key
    
    # Check if we have a cached value
    if cache_key in _config_cache:
        return _config_cache[cache_key]
    
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/support-config/key/{key}"
            params = {"organization_id": organization_id} if organization_id else {}
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            config = response.json()
            value = json.loads(config["value"])
            
            # Cache the value
            _config_cache[cache_key] = value
            return value
    except httpx.RequestError as e:
        # Log the error and return default values
        print(f"Error connecting to super admin API: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "ticket_priorities": ["Low", "Medium", "High", "Urgent"],
            "ticket_statuses": ["New", "Open", "Pending", "Resolved", "Closed", "Escalated"],
            "ticket_channels": ["Email", "Phone", "Chat", "Portal", "Social Media"],
            "sla_priorities": ["Low", "Medium", "High", "Urgent"],
            "kb_categories": ["General", "Technical", "Billing", "Account", "Product", "Troubleshooting"],
            "interaction_types": ["Call", "Email", "Chat", "Meeting", "Note"],
            "chat_statuses": ["Available", "Busy", "Away", "Offline"],
            "report_types": ["Ticket Volume", "Resolution Time", "Agent Performance", "Customer Satisfaction", "SLA Compliance", "Channel Performance"]
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "ticket_priorities": ["Low", "Medium", "High", "Urgent"],
            "ticket_statuses": ["New", "Open", "Pending", "Resolved", "Closed", "Escalated"],
            "ticket_channels": ["Email", "Phone", "Chat", "Portal", "Social Media"],
            "sla_priorities": ["Low", "Medium", "High", "Urgent"],
            "kb_categories": ["General", "Technical", "Billing", "Account", "Product", "Troubleshooting"],
            "interaction_types": ["Call", "Email", "Chat", "Meeting", "Note"],
            "chat_statuses": ["Available", "Busy", "Away", "Offline"],
            "report_types": ["Ticket Volume", "Resolution Time", "Agent Performance", "Customer Satisfaction", "SLA Compliance", "Channel Performance"]
        }
        
        return defaults.get(key, None)

def clear_config_cache():
    """Clear the configuration cache"""
    global _config_cache
    _config_cache.clear()

async def refresh_config_cache():
    """Refresh the configuration cache by clearing it"""
    clear_config_cache()

def get_support_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a support configuration value by key.
    
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
    return loop.run_until_complete(get_support_config_from_superadmin(key, organization_id))

def get_ticket_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket priorities"""
    return get_support_config("ticket_priorities", organization_id)

def get_ticket_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket statuses"""
    return get_support_config("ticket_statuses", organization_id)

def get_ticket_channels(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket channels"""
    return get_support_config("ticket_channels", organization_id)

def get_sla_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available SLA priorities"""
    return get_support_config("sla_priorities", organization_id)

def get_kb_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available knowledge base categories"""
    return get_support_config("kb_categories", organization_id)

def get_interaction_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available interaction types"""
    return get_support_config("interaction_types", organization_id)

def get_chat_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available chat agent statuses"""
    return get_support_config("chat_statuses", organization_id)

def get_report_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available report types"""
    return get_support_config("report_types", organization_id)