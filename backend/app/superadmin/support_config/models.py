from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SupportConfigBase(BaseModel):
    key: str
    value: str
    description: str
    category: str
    organization_id: Optional[int] = None

class SupportConfigCreate(SupportConfigBase):
    pass

class SupportConfigUpdate(SupportConfigBase):
    pass

class SupportConfig(SupportConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None