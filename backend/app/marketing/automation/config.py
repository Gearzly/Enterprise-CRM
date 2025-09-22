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
            "workflow_statuses": ["Draft", "Active", "Paused", "Completed", "Error"],
            "trigger_types": [
                "Form Submission",
                "Email Open",
                "Email Click",
                "Website Visit",
                "Download",
                "Purchase",
                "Webinar Attendance",
                "Custom Event"
            ],
            "action_types": [
                "Send Email",
                "Update Contact",
                "Add Tag",
                "Remove Tag",
                "Assign Owner",
                "Send Notification",
                "Add to List",
                "Remove from List",
                "Score Lead",
                "Create Task",
                "Custom Action"
            ],
            "default_execution_count": 0,
            "default_score_threshold": 50,
            "max_workflow_steps": 50
        }
        
        return defaults.get(key, None)
    except Exception as e:
        # Log the error and return default values
        print(f"Error fetching config from super admin: {e}")
        
        # Default values if super admin is unreachable
        defaults = {
            "workflow_statuses": ["Draft", "Active", "Paused", "Completed", "Error"],
            "trigger_types": [
                "Form Submission",
                "Email Open",
                "Email Click",
                "Website Visit",
                "Download",
                "Purchase",
                "Webinar Attendance",
                "Custom Event"
            ],
            "action_types": [
                "Send Email",
                "Update Contact",
                "Add Tag",
                "Remove Tag",
                "Assign Owner",
                "Send Notification",
                "Add to List",
                "Remove from List",
                "Score Lead",
                "Create Task",
                "Custom Action"
            ],
            "default_execution_count": 0,
            "default_score_threshold": 50,
            "max_workflow_steps": 50
        }
        
        return defaults.get(key, None)

def get_automation_config(key: str, organization_id: Optional[int] = None) -> Any:
    """
    Get an automation configuration value by key.
    
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

def get_workflow_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available workflow statuses"""
    return get_automation_config("workflow_statuses", organization_id)

def get_trigger_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available trigger types"""
    return get_automation_config("trigger_types", organization_id)

def get_action_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available action types"""
    return get_automation_config("action_types", organization_id)

def get_default_execution_count(organization_id: Optional[int] = None) -> int:
    """Get default execution count"""
    return get_automation_config("default_execution_count", organization_id)

def get_default_score_threshold(organization_id: Optional[int] = None) -> int:
    """Get default score threshold"""
    return get_automation_config("default_score_threshold", organization_id)

def get_max_workflow_steps(organization_id: Optional[int] = None) -> int:
    """Get maximum workflow steps"""
    return get_automation_config("max_workflow_steps", organization_id)