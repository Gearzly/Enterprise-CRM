import json
import httpx
from typing import List, Optional
from app.core.config.dynamic_config import get_sales_default, get_config_value

def get_lead_statuses(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead statuses"""
    value = get_config_value("sales.lead_statuses", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["New", "Contacted", "Qualified", "Unqualified", "Converted"]

def get_lead_sources(organization_id: Optional[int] = None) -> List[str]:
    """Get available lead sources"""
    value = get_config_value("sales.lead_sources", organization_id)
    # Ensure we return a list, even if the config returns None
    return value if value is not None else ["Website", "Referral", "Social Media", "Email Campaign", "Event", "Other"]
