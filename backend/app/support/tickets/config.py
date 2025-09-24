import json
import httpx
from typing import List, Optional
from app.core.config.dynamic_config import get_config_value

def get_ticket_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket priorities"""
    value = get_config_value("support.ticket_priorities", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Low", "Medium", "High", "Urgent"]

def get_ticket_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket statuses"""
    value = get_config_value("support.ticket_statuses", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["New", "Open", "Pending", "Resolved", "Closed", "Escalated"]

def get_ticket_channels(organization_id: Optional[int] = None) -> List[str]:
    """Get available ticket channels"""
    value = get_config_value("support.ticket_channels", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Email", "Phone", "Chat", "Portal", "Social Media"]

def get_sla_priorities(organization_id: Optional[int] = None) -> List[str]:
    """Get available SLA priorities"""
    value = get_config_value("support.sla_priorities", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Low", "Medium", "High", "Urgent"]

def get_kb_categories(organization_id: Optional[int] = None) -> List[str]:
    """Get available knowledge base categories"""
    value = get_config_value("support.kb_categories", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["General", "Technical", "Billing", "Account", "Product", "Troubleshooting"]

def get_interaction_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available interaction types"""
    value = get_config_value("support.interaction_types", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Call", "Email", "Chat", "Meeting", "Note"]

def get_chat_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available chat agent statuses"""
    value = get_config_value("support.chat_statuses", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Available", "Busy", "Away", "Offline"]

def get_report_types(organization_id: Optional[int] = None) -> List[str]:
    """Get available report types"""
    value = get_config_value("support.report_types", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Ticket Volume", "Resolution Time", "Agent Performance", "Customer Satisfaction", "SLA Compliance", "Channel Performance"]
