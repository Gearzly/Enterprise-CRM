from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class MarketingConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    category: str
    organization_id: Optional[int] = None  # None for global, specific ID for org-specific

class MarketingConfigCreate(MarketingConfigBase):
    pass

class MarketingConfigUpdate(MarketingConfigBase):
    pass

class MarketingConfig(MarketingConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None