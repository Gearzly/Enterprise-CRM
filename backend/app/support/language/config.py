import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

async def get_language_config_from_superadmin(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a language configuration value by key from the super admin service.
    
    Args:
        key: The configuration key to retrieve
        organization_id: Optional organization ID for org-specific configs
    
    Returns:
        The configuration value
    """
    try:
        # Make actual HTTP request to super admin API
        async with httpx.AsyncClient() as client:
            url = f"http://superadmin-service/api/v1/language-config/key/{key}"
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
            "supported_languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar"],
            "default_language": "en",
            "translation_statuses": ["Pending", "Translated", "Reviewed", "Published"],
            "max_confidence_threshold": 0.8,
            "min_confidence_threshold": 0.5
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "supported_languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar"],
            "default_language": "en",
            "translation_statuses": ["Pending", "Translated", "Reviewed", "Published"],
            "max_confidence_threshold": 0.8,
            "min_confidence_threshold": 0.5
        }
        
        return defaults.get(key, None)

def get_language_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get a language configuration value by key.
    
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
    return loop.run_until_complete(get_language_config_from_superadmin(key, organization_id))

def get_supported_languages(organization_id: Optional[int] = None) -> List[str]:
    """Get supported languages"""
    return get_language_config("supported_languages", organization_id)

def get_default_language(organization_id: Optional[int] = None) -> str:
    """Get default language"""
    return get_language_config("default_language", organization_id)

def get_translation_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available translation statuses"""
    return get_language_config("translation_statuses", organization_id)

def get_max_confidence_threshold(organization_id: Optional[int] = None) -> float:
    """Get maximum confidence threshold for language detection"""
    return get_language_config("max_confidence_threshold", organization_id)

def get_min_confidence_threshold(organization_id: Optional[int] = None) -> float:
    """Get minimum confidence threshold for language detection"""
    return get_language_config("min_confidence_threshold", organization_id)