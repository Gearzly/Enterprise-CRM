"""
Dynamic Configuration Utilities

This module provides utilities for fetching dynamic configuration values
and applying them to model defaults.
"""

import json
import httpx
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from functools import lru_cache
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuration cache to reduce API calls
_config_cache: Dict[str, Any] = {}
_cache_expiry: Dict[str, datetime] = {}

# Cache timeout in seconds (5 minutes)
CACHE_TIMEOUT = 300

def _is_cache_expired(cache_key: str) -> bool:
    """Check if a cache entry has expired"""
    if cache_key not in _cache_expiry:
        return True
    return (datetime.now() - _cache_expiry[cache_key]).seconds > CACHE_TIMEOUT

def _get_cache_key(key: str, organization_id: Optional[int] = None) -> str:
    """Generate a cache key"""
    return f"{key}:{organization_id}" if organization_id else key

async def _fetch_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Fetch a configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    # Create a cache key
    cache_key = _get_cache_key(key, organization_id)
    
    # Check if we have a cached value that hasn't expired
    if cache_key in _config_cache and not _is_cache_expired(cache_key):
        return _config_cache[cache_key]
    
    try:
        # Make actual HTTP request to super admin API
        # Note: In a real implementation, this would point to the actual super admin service
        async with httpx.AsyncClient() as client:
            # For demo purposes, we'll use a mock URL
            # In production, this would be the actual super admin service URL
            url = f"http://superadmin-service/api/v1/config/{key}"
            params = {"organization_id": organization_id} if organization_id else {}
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            config = response.json()
            value = json.loads(config["value"])
            
            # Cache the value with expiration
            _config_cache[cache_key] = value
            _cache_expiry[cache_key] = datetime.now()
            return value
    except (httpx.RequestError, httpx.HTTPStatusError, KeyError) as e:
        # Log the error
        logger.warning(f"Error fetching config from super admin: {e}")
        return None

def get_config_value(key: str, organization_id: Optional[int] = None, default: Any = None) -> Any:
    """
    Get a configuration value by key, with fallback to default.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
        default: Default value to return if config is not found
        
    Returns:
        The configuration value or default
    """
    try:
        # Try to get the running event loop
        loop = asyncio.get_running_loop()
        # Run the async function in the existing loop
        future = asyncio.run_coroutine_threadsafe(
            _fetch_config_from_superadmin(key, organization_id), loop
        )
        return future.result(timeout=10.0)
    except (RuntimeError, asyncio.TimeoutError):
        # If no event loop is running or timeout, return default
        logger.warning(f"Timeout or no event loop for config key: {key}")
        return default
    except Exception as e:
        # Log the error and return default
        logger.error(f"Error getting config value for key {key}: {e}")
        return default

# Sales Configuration Utilities
def get_sales_default(key: str, organization_id: Optional[int] = None) -> Any:
    """Get sales configuration default values"""
    defaults = {
        "lead_status": "New",
        "lead_source": "Website",
        "opportunity_stage": "Prospecting",
        "quotation_status": "Draft",
        "contact_type": "Primary",
        "activity_status": "Pending",
        "report_status": "Draft",
        "default_tax_rate": 0.0,
    }
    
    # Try to get dynamic value first
    dynamic_value = get_config_value(f"sales.{key}", organization_id)
    if dynamic_value is not None:
        return dynamic_value
    
    # Return default if no dynamic value found
    return defaults.get(key, None)

# Marketing Configuration Utilities
def get_marketing_default(key: str, organization_id: Optional[int] = None) -> Any:
    """Get marketing configuration default values"""
    defaults = {
        "campaign_status": "Draft",
        "lead_status": "New",
        "lead_source": "Website",
        "email_category": "Newsletter",
        "template_status": "Draft",
    }
    
    # Try to get dynamic value first
    dynamic_value = get_config_value(f"marketing.{key}", organization_id)
    if dynamic_value is not None:
        return dynamic_value
    
    # Return default if no dynamic value found
    return defaults.get(key, None)

# Support Configuration Utilities
def get_support_default(key: str, organization_id: Optional[int] = None) -> Any:
    """Get support configuration default values"""
    defaults = {
        "ticket_priority": "Medium",
        "ticket_status": "New",
        "ticket_channel": "Email",
        "sla_status": "Active",
    }
    
    # Try to get dynamic value first
    dynamic_value = get_config_value(f"support.{key}", organization_id)
    if dynamic_value is not None:
        return dynamic_value
    
    # Return default if no dynamic value found
    return defaults.get(key, None)

# System Configuration Utilities
def get_system_default(key: str, organization_id: Optional[int] = None) -> Any:
    """Get system configuration default values"""
    defaults = {
        "max_file_upload_size": "10MB",
        "data_retention_period": 365,
        "email_provider": "smtp",
    }
    
    # Try to get dynamic value first
    dynamic_value = get_config_value(f"system.{key}", organization_id)
    if dynamic_value is not None:
        return dynamic_value
    
    # Return default if no dynamic value found
    return defaults.get(key, None)

# Cache Management
def clear_config_cache():
    """Clear the configuration cache"""
    global _config_cache, _cache_expiry
    _config_cache.clear()
    _cache_expiry.clear()

def refresh_config_cache():
    """Refresh the configuration cache by clearing it"""
    clear_config_cache()

# Utility function to get all defaults for a module
def get_module_defaults(module: str, organization_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Get all default values for a specific module.
    
    Args:
        module: Module name (sales, marketing, support, system)
        organization_id: Optional organization ID for org-specific configs
        
    Returns:
        Dictionary of default values
    """
    if module == "sales":
        return {
            "lead_status": get_sales_default("lead_status", organization_id),
            "lead_source": get_sales_default("lead_source", organization_id),
            "opportunity_stage": get_sales_default("opportunity_stage", organization_id),
            "quotation_status": get_sales_default("quotation_status", organization_id),
            "contact_type": get_sales_default("contact_type", organization_id),
            "activity_status": get_sales_default("activity_status", organization_id),
            "report_status": get_sales_default("report_status", organization_id),
            "default_tax_rate": get_sales_default("default_tax_rate", organization_id),
        }
    elif module == "marketing":
        return {
            "campaign_status": get_marketing_default("campaign_status", organization_id),
            "lead_status": get_marketing_default("lead_status", organization_id),
            "lead_source": get_marketing_default("lead_source", organization_id),
            "email_category": get_marketing_default("email_category", organization_id),
            "template_status": get_marketing_default("template_status", organization_id),
        }
    elif module == "support":
        return {
            "ticket_priority": get_support_default("ticket_priority", organization_id),
            "ticket_status": get_support_default("ticket_status", organization_id),
            "ticket_channel": get_support_default("ticket_channel", organization_id),
            "sla_status": get_support_default("sla_status", organization_id),
        }
    elif module == "system":
        return {
            "max_file_upload_size": get_system_default("max_file_upload_size", organization_id),
            "data_retention_period": get_system_default("data_retention_period", organization_id),
            "email_provider": get_system_default("email_provider", organization_id),
        }
    else:
        return {}