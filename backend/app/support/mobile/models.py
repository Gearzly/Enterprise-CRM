from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MobileDeviceBase(BaseModel):
    device_id: str
    user_id: int
    device_type: str
    app_type: str
    os_version: str
    app_version: str
    is_active: bool = True

class MobileDeviceCreate(MobileDeviceBase):
    pass

class MobileDeviceUpdate(MobileDeviceBase):
    pass

class MobileDevice(MobileDeviceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None

class MobileTicketBase(BaseModel):
    device_id: str
    customer_id: int
    subject: str
    description: str
    priority: str
    status: str = "Offline Created"
    location: Optional[str] = None
    offline_data: Optional[str] = None

class MobileTicketCreate(MobileTicketBase):
    pass

class MobileTicketUpdate(MobileTicketBase):
    pass

class MobileTicket(MobileTicketBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    synced_at: Optional[datetime] = None

class MobileNotificationBase(BaseModel):
    device_id: str
    title: str
    message: str
    is_read: bool = False
    action_url: Optional[str] = None

class MobileNotificationCreate(MobileNotificationBase):
    pass

class MobileNotification(MobileNotificationBase):
    id: int
    created_at: datetime

class MobileAttachmentBase(BaseModel):
    ticket_id: int
    file_name: str
    file_type: str
    file_size: int
    local_path: str
    is_synced: bool = False

class MobileAttachmentCreate(MobileAttachmentBase):
    pass

class MobileAttachment(MobileAttachmentBase):
    id: int
    created_at: datetime
    synced_at: Optional[datetime] = None

class MobileLocationBase(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: datetime

class MobileLocationCreate(MobileLocationBase):
    pass

class MobileLocation(MobileLocationBase):
    id: int