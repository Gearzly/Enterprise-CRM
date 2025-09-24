from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    MobileDevice, MobileDeviceCreate, MobileDeviceUpdate,
    MobileTicket, MobileTicketCreate, MobileTicketUpdate,
    MobileNotification, MobileNotificationCreate,
    MobileAttachment, MobileAttachmentCreate,
    MobileLocation, MobileLocationCreate
)
from .config import (
    get_mobile_device_types, get_mobile_app_types, get_mobile_ticket_statuses,
    get_default_device_type, get_default_app_type, get_max_attachment_size_mb
)

router = APIRouter()

# In-memory storage for demo purposes
mobile_devices_db = []
mobile_tickets_db = []
mobile_notifications_db = []
mobile_attachments_db = []
mobile_locations_db = []

@router.get("/devices", response_model=List[MobileDevice])
def list_mobile_devices():
    """List all mobile devices"""
    return mobile_devices_db

@router.get("/devices/{device_id}", response_model=MobileDevice)
def get_mobile_device(device_id: str):
    """Get a specific mobile device by ID"""
    for device in mobile_devices_db:
        if device.device_id == device_id:
            return device
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.post("/devices", response_model=MobileDevice)
def register_mobile_device(device: MobileDeviceCreate):
    """Register a new mobile device"""
    # Check if device already exists
    for existing_device in mobile_devices_db:
        if existing_device.device_id == device.device_id:
            raise HTTPException(status_code=400, detail="Device already registered")
    
    new_device = MobileDevice(
        id=len(mobile_devices_db) + 1,
        created_at=datetime.now(),
        **device.dict()
    )
    mobile_devices_db.append(new_device)
    return new_device

@router.put("/devices/{device_id}", response_model=MobileDevice)
def update_mobile_device(device_id: str, device_update: MobileDeviceUpdate):
    """Update an existing mobile device"""
    for index, device in enumerate(mobile_devices_db):
        if device.device_id == device_id:
            updated_device = MobileDevice(
                id=device.id,
                created_at=device.created_at,
                updated_at=datetime.now(),
                **device_update.dict()
            )
            mobile_devices_db[index] = updated_device
            return updated_device
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.delete("/devices/{device_id}")
def unregister_mobile_device(device_id: str):
    """Unregister a mobile device"""
    for index, device in enumerate(mobile_devices_db):
        if device.device_id == device_id:
            del mobile_devices_db[index]
            return {"message": "Mobile device unregistered successfully"}
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.post("/devices/{device_id}/activate")
def activate_mobile_device(device_id: str):
    """Activate a mobile device"""
    for index, device in enumerate(mobile_devices_db):
        if device.device_id == device_id:
            mobile_devices_db[index].is_active = True
            return {"message": "Mobile device activated successfully"}
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.post("/devices/{device_id}/deactivate")
def deactivate_mobile_device(device_id: str):
    """Deactivate a mobile device"""
    for index, device in enumerate(mobile_devices_db):
        if device.device_id == device_id:
            mobile_devices_db[index].is_active = False
            return {"message": "Mobile device deactivated successfully"}
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.post("/devices/{device_id}/ping")
def ping_mobile_device(device_id: str):
    """Ping a mobile device to update last seen timestamp"""
    for index, device in enumerate(mobile_devices_db):
        if device.device_id == device_id:
            mobile_devices_db[index].last_seen_at = datetime.now()
            return {"message": "Mobile device ping successful"}
    raise HTTPException(status_code=404, detail="Mobile device not found")

@router.get("/devices/user/{user_id}", response_model=List[MobileDevice])
def get_devices_by_user(user_id: int):
    """Get mobile devices by user ID"""
    return [device for device in mobile_devices_db if device.user_id == user_id]

@router.get("/devices/type/{type}", response_model=List[MobileDevice])
def get_mobile_devices_by_type(type: str):
    """Get mobile devices by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [device for device in mobile_devices_db if device.device_type == normalized_type]

# Mobile Ticket endpoints
@router.get("/tickets", response_model=List[MobileTicket])
def list_mobile_tickets():
    """List all mobile tickets"""
    return mobile_tickets_db

@router.get("/tickets/{ticket_id}", response_model=MobileTicket)
def get_mobile_ticket(ticket_id: int):
    """Get a specific mobile ticket by ID"""
    for ticket in mobile_tickets_db:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Mobile ticket not found")

@router.post("/tickets", response_model=MobileTicket)
def create_mobile_ticket(ticket: MobileTicketCreate):
    """Create a new mobile ticket"""
    new_id = max([t.id for t in mobile_tickets_db]) + 1 if mobile_tickets_db else 1
    new_ticket = MobileTicket(
        id=new_id,
        created_at=datetime.now(),
        **ticket.dict()
    )
    mobile_tickets_db.append(new_ticket)
    return new_ticket

@router.put("/tickets/{ticket_id}", response_model=MobileTicket)
def update_mobile_ticket(ticket_id: int, ticket_update: MobileTicketUpdate):
    """Update an existing mobile ticket"""
    for index, ticket in enumerate(mobile_tickets_db):
        if ticket.id == ticket_id:
            updated_ticket = MobileTicket(
                id=ticket_id,
                created_at=ticket.created_at,
                updated_at=datetime.now(),
                **ticket_update.dict()
            )
            mobile_tickets_db[index] = updated_ticket
            return updated_ticket
    raise HTTPException(status_code=404, detail="Mobile ticket not found")

@router.delete("/tickets/{ticket_id}")
def delete_mobile_ticket(ticket_id: int):
    """Delete a mobile ticket"""
    for index, ticket in enumerate(mobile_tickets_db):
        if ticket.id == ticket_id:
            del mobile_tickets_db[index]
            return {"message": "Mobile ticket deleted successfully"}
    raise HTTPException(status_code=404, detail="Mobile ticket not found")

@router.post("/tickets/{ticket_id}/sync")
def sync_mobile_ticket(ticket_id: int):
    """Sync a mobile ticket with the main system"""
    for index, ticket in enumerate(mobile_tickets_db):
        if ticket.id == ticket_id:
            mobile_tickets_db[index].status = "Synced"
            mobile_tickets_db[index].synced_at = datetime.now()
            return {"message": "Mobile ticket synced successfully"}
    raise HTTPException(status_code=404, detail="Mobile ticket not found")

@router.get("/tickets/device/{device_id}", response_model=List[MobileTicket])
def get_tickets_by_device(device_id: str):
    """Get mobile tickets by device ID"""
    return [ticket for ticket in mobile_tickets_db if ticket.device_id == device_id]

@router.get("/tickets/customer/{customer_id}", response_model=List[MobileTicket])
def get_tickets_by_customer(customer_id: int):
    """Get mobile tickets by customer ID"""
    return [ticket for ticket in mobile_tickets_db if ticket.customer_id == customer_id]

@router.get("/tickets/status/{status}", response_model=List[MobileTicket])
def get_mobile_tickets_by_status(status: str):
    """Get mobile tickets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [ticket for ticket in mobile_tickets_db if ticket.status == normalized_status]

# Mobile Notification endpoints
@router.get("/notifications", response_model=List[MobileNotification])
def list_mobile_notifications():
    """List all mobile notifications"""
    return mobile_notifications_db

@router.get("/notifications/{notification_id}", response_model=MobileNotification)
def get_mobile_notification(notification_id: int):
    """Get a specific mobile notification by ID"""
    for notification in mobile_notifications_db:
        if notification.id == notification_id:
            return notification
    raise HTTPException(status_code=404, detail="Mobile notification not found")

@router.post("/notifications", response_model=MobileNotification)
def create_mobile_notification(notification: MobileNotificationCreate):
    """Create a new mobile notification"""
    new_id = max([n.id for n in mobile_notifications_db]) + 1 if mobile_notifications_db else 1
    new_notification = MobileNotification(
        id=new_id,
        created_at=datetime.now(),
        **notification.dict()
    )
    mobile_notifications_db.append(new_notification)
    return new_notification

@router.put("/notifications/{notification_id}/read")
def mark_notification_as_read(notification_id: int):
    """Mark a mobile notification as read"""
    for index, notification in enumerate(mobile_notifications_db):
        if notification.id == notification_id:
            mobile_notifications_db[index].is_read = True
            return {"message": "Mobile notification marked as read"}
    raise HTTPException(status_code=404, detail="Mobile notification not found")

@router.get("/notifications/device/{device_id}", response_model=List[MobileNotification])
def get_notifications_for_device(device_id: str):
    """Get notifications for a specific device"""
    return [notification for notification in mobile_notifications_db if notification.device_id == device_id]

@router.get("/notifications/unread/device/{device_id}", response_model=List[MobileNotification])
def get_unread_notifications_for_device(device_id: str):
    """Get unread notifications for a specific device"""
    return [notification for notification in mobile_notifications_db 
            if notification.device_id == device_id and not notification.is_read]

# Mobile Attachment endpoints
@router.get("/attachments", response_model=List[MobileAttachment])
def list_mobile_attachments():
    """List all mobile attachments"""
    return mobile_attachments_db

@router.get("/attachments/{attachment_id}", response_model=MobileAttachment)
def get_mobile_attachment(attachment_id: int):
    """Get a specific mobile attachment by ID"""
    for attachment in mobile_attachments_db:
        if attachment.id == attachment_id:
            return attachment
    raise HTTPException(status_code=404, detail="Mobile attachment not found")

@router.post("/attachments", response_model=MobileAttachment)
def create_mobile_attachment(attachment: MobileAttachmentCreate):
    """Create a new mobile attachment"""
    new_id = max([a.id for a in mobile_attachments_db]) + 1 if mobile_attachments_db else 1
    new_attachment = MobileAttachment(
        id=new_id,
        created_at=datetime.now(),
        **attachment.dict()
    )
    mobile_attachments_db.append(new_attachment)
    return new_attachment

@router.post("/attachments/{attachment_id}/sync")
def sync_mobile_attachment(attachment_id: int):
    """Sync a mobile attachment with the main system"""
    for index, attachment in enumerate(mobile_attachments_db):
        if attachment.id == attachment_id:
            mobile_attachments_db[index].is_synced = True
            mobile_attachments_db[index].synced_at = datetime.now()
            return {"message": "Mobile attachment synced successfully"}
    raise HTTPException(status_code=404, detail="Mobile attachment not found")

@router.get("/attachments/ticket/{ticket_id}", response_model=List[MobileAttachment])
def get_attachments_for_ticket(ticket_id: int):
    """Get attachments for a specific ticket"""
    return [attachment for attachment in mobile_attachments_db if attachment.ticket_id == ticket_id]

@router.get("/attachments/unsynced", response_model=List[MobileAttachment])
def get_unsynced_attachments():
    """Get all unsynced attachments"""
    return [attachment for attachment in mobile_attachments_db if not attachment.is_synced]

# Mobile Location endpoints
@router.get("/locations", response_model=List[MobileLocation])
def list_mobile_locations():
    """List all mobile locations"""
    return mobile_locations_db

@router.get("/locations/{location_id}", response_model=MobileLocation)
def get_mobile_location(location_id: int):
    """Get a specific mobile location by ID"""
    for location in mobile_locations_db:
        if location.id == location_id:
            return location
    raise HTTPException(status_code=404, detail="Mobile location not found")

@router.post("/locations", response_model=MobileLocation)
def create_mobile_location(location: MobileLocationCreate):
    """Create a new mobile location"""
    new_id = max([l.id for l in mobile_locations_db]) + 1 if mobile_locations_db else 1
    new_location = MobileLocation(
        id=new_id,
        **location.dict()
    )
    mobile_locations_db.append(new_location)
    return new_location

@router.get("/locations/device/{device_id}", response_model=List[MobileLocation])
def get_locations_for_device(device_id: str):
    """Get locations for a specific device"""
    return [location for location in mobile_locations_db if location.device_id == device_id]

@router.get("/locations/latest/device/{device_id}", response_model=MobileLocation)
def get_latest_location_for_device(device_id: str):
    """Get the latest location for a specific device"""
    device_locations = [location for location in mobile_locations_db if location.device_id == device_id]
    if not device_locations:
        raise HTTPException(status_code=404, detail="No locations found for device")
    return max(device_locations, key=lambda x: x.timestamp)

# Configuration endpoints
@router.get("/config/device-types", response_model=List[str])
def get_mobile_device_type_options():
    """Get available mobile device type options"""
    return get_mobile_device_types()

@router.get("/config/app-types", response_model=List[str])
def get_mobile_app_type_options():
    """Get available mobile app type options"""
    return get_mobile_app_types()

@router.get("/config/ticket-statuses", response_model=List[str])
def get_mobile_ticket_status_options():
    """Get available mobile ticket status options"""
    return get_mobile_ticket_statuses()

@router.get("/config/max-attachment-size", response_model=int)
def get_max_attachment_size():
    """Get maximum attachment size in MB"""
    return get_max_attachment_size_mb()