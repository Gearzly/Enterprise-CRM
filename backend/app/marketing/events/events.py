from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    Event, EventCreate, EventUpdate,
    Registration, RegistrationCreate, RegistrationUpdate,
    EventPromotion, EventPromotionCreate, EventPromotionUpdate,
    AttendeeEngagement, AttendeeEngagementCreate, AttendeeEngagementUpdate,
    PostEventFollowUp, PostEventFollowUpCreate, PostEventFollowUpUpdate
)
from .config import (
    get_event_statuses, get_event_types,
    get_default_registered_count, get_default_attended_count
)

router = APIRouter()

# In-memory storage for demo purposes
events_db = []
registrations_db = []
event_promotions_db = []
attendee_engagements_db = []
post_event_follow_ups_db = []

@router.get("/events", response_model=List[Event])
def list_events():
    """List all events"""
    return events_db

@router.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    """Get a specific event by ID"""
    for event in events_db:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.post("/events", response_model=Event)
def create_event(event: EventCreate):
    """Create a new event"""
    new_id = max([e.id for e in events_db]) + 1 if events_db else 1
    new_event = Event(
        id=new_id,
        created_at=datetime.now(),
        registered_count=get_default_registered_count(),
        attended_count=get_default_attended_count(),
        **event.dict()
    )
    events_db.append(new_event)
    return new_event

@router.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event_update: EventUpdate):
    """Update an existing event"""
    for index, event in enumerate(events_db):
        if event.id == event_id:
            updated_event = Event(
                id=event_id,
                created_at=event.created_at,
                updated_at=datetime.now(),
                registered_count=event.registered_count,
                attended_count=event.attended_count,
                **event_update.dict()
            )
            events_db[index] = updated_event
            return updated_event
    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    """Delete an event"""
    for index, event in enumerate(events_db):
        if event.id == event_id:
            del events_db[index]
            return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=404, detail="Event not found")

@router.get("/events/status/{status}", response_model=List[Event])
def get_events_by_status(status: str):
    """Get events by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [event for event in events_db if event.status == normalized_status]

@router.get("/events/type/{event_type}", response_model=List[Event])
def get_events_by_type(event_type: str):
    """Get events by type"""
    # Normalize the event_type parameter to handle case differences
    normalized_type = event_type.lower().title()
    return [event for event in events_db if event.event_type == normalized_type]

@router.post("/events/{event_id}/open-registration")
def open_event_registration(event_id: int):
    """Open registration for an event"""
    for index, event in enumerate(events_db):
        if event.id == event_id:
            event.status = "Registration Open"
            events_db[index] = event
            return {"message": f"Registration opened for event {event_id}"}
    raise HTTPException(status_code=404, detail="Event not found")

@router.post("/events/{event_id}/close-registration")
def close_event_registration(event_id: int):
    """Close registration for an event"""
    for index, event in enumerate(events_db):
        if event.id == event_id:
            event.status = "Upcoming"
            events_db[index] = event
            return {"message": f"Registration closed for event {event_id}"}
    raise HTTPException(status_code=404, detail="Event not found")

# Registrations endpoints
@router.get("/registrations", response_model=List[Registration])
def list_registrations():
    """List all registrations"""
    return registrations_db

@router.get("/registrations/{registration_id}", response_model=Registration)
def get_registration(registration_id: int):
    """Get a specific registration by ID"""
    for registration in registrations_db:
        if registration.id == registration_id:
            return registration
    raise HTTPException(status_code=404, detail="Registration not found")

@router.post("/registrations", response_model=Registration)
def create_registration(registration: RegistrationCreate):
    """Create a new registration"""
    new_id = max([r.id for r in registrations_db]) + 1 if registrations_db else 1
    new_registration = Registration(
        id=new_id,
        created_at=datetime.now(),
        **registration.dict()
    )
    registrations_db.append(new_registration)
    
    # Update event registered count
    for event in events_db:
        if event.id == registration.event_id:
            event.registered_count += 1
            break
    
    return new_registration

@router.put("/registrations/{registration_id}", response_model=Registration)
def update_registration(registration_id: int, registration_update: RegistrationUpdate):
    """Update an existing registration"""
    for index, registration in enumerate(registrations_db):
        if registration.id == registration_id:
            updated_registration = Registration(
                id=registration_id,
                created_at=registration.created_at,
                updated_at=datetime.now(),
                **registration_update.dict()
            )
            registrations_db[index] = updated_registration
            return updated_registration
    raise HTTPException(status_code=404, detail="Registration not found")

@router.delete("/registrations/{registration_id}")
def delete_registration(registration_id: int):
    """Delete a registration"""
    for index, registration in enumerate(registrations_db):
        if registration.id == registration_id:
            del registrations_db[index]
            return {"message": "Registration deleted successfully"}
    raise HTTPException(status_code=404, detail="Registration not found")

@router.post("/registrations/{registration_id}/confirm")
def confirm_registration(registration_id: int):
    """Confirm a registration"""
    for index, registration in enumerate(registrations_db):
        if registration.id == registration_id:
            registration.is_confirmed = True
            registrations_db[index] = registration
            return {"message": f"Registration {registration_id} confirmed"}
    raise HTTPException(status_code=404, detail="Registration not found")

@router.post("/registrations/{registration_id}/check-in")
def check_in_registration(registration_id: int):
    """Check in a registration"""
    for index, registration in enumerate(registrations_db):
        if registration.id == registration_id:
            registration.check_in_time = datetime.now()
            registrations_db[index] = registration
            
            # Update event attended count
            for event in events_db:
                if event.id == registration.event_id:
                    event.attended_count += 1
                    break
                    
            return {"message": f"Registration {registration_id} checked in"}
    raise HTTPException(status_code=404, detail="Registration not found")

@router.get("/registrations/event/{event_id}", response_model=List[Registration])
def get_registrations_by_event(event_id: int):
    """Get registrations by event ID"""
    return [registration for registration in registrations_db if registration.event_id == event_id]

# Event Promotions endpoints
@router.get("/promotions", response_model=List[EventPromotion])
def list_event_promotions():
    """List all event promotions"""
    return event_promotions_db

@router.get("/promotions/{promotion_id}", response_model=EventPromotion)
def get_event_promotion(promotion_id: int):
    """Get a specific event promotion by ID"""
    for promotion in event_promotions_db:
        if promotion.id == promotion_id:
            return promotion
    raise HTTPException(status_code=404, detail="Event promotion not found")

@router.post("/promotions", response_model=EventPromotion)
def create_event_promotion(promotion: EventPromotionCreate):
    """Create a new event promotion"""
    new_id = max([p.id for p in event_promotions_db]) + 1 if event_promotions_db else 1
    new_promotion = EventPromotion(
        id=new_id,
        created_at=datetime.now(),
        reach=0,
        clicks=0,
        conversions=0,
        **promotion.dict()
    )
    event_promotions_db.append(new_promotion)
    return new_promotion

@router.put("/promotions/{promotion_id}", response_model=EventPromotion)
def update_event_promotion(promotion_id: int, promotion_update: EventPromotionUpdate):
    """Update an existing event promotion"""
    for index, promotion in enumerate(event_promotions_db):
        if promotion.id == promotion_id:
            updated_promotion = EventPromotion(
                id=promotion_id,
                created_at=promotion.created_at,
                updated_at=datetime.now(),
                reach=promotion.reach,
                clicks=promotion.clicks,
                conversions=promotion.conversions,
                **promotion_update.dict()
            )
            event_promotions_db[index] = updated_promotion
            return updated_promotion
    raise HTTPException(status_code=404, detail="Event promotion not found")

@router.delete("/promotions/{promotion_id}")
def delete_event_promotion(promotion_id: int):
    """Delete an event promotion"""
    for index, promotion in enumerate(event_promotions_db):
        if promotion.id == promotion_id:
            del event_promotions_db[index]
            return {"message": "Event promotion deleted successfully"}
    raise HTTPException(status_code=404, detail="Event promotion not found")

# Attendee Engagements endpoints
@router.get("/engagements", response_model=List[AttendeeEngagement])
def list_attendee_engagements():
    """List all attendee engagements"""
    return attendee_engagements_db

@router.get("/engagements/{engagement_id}", response_model=AttendeeEngagement)
def get_attendee_engagement(engagement_id: int):
    """Get a specific attendee engagement by ID"""
    for engagement in attendee_engagements_db:
        if engagement.id == engagement_id:
            return engagement
    raise HTTPException(status_code=404, detail="Attendee engagement not found")

@router.post("/engagements", response_model=AttendeeEngagement)
def create_attendee_engagement(engagement: AttendeeEngagementCreate):
    """Create a new attendee engagement"""
    new_id = max([e.id for e in attendee_engagements_db]) + 1 if attendee_engagements_db else 1
    new_engagement = AttendeeEngagement(
        id=new_id,
        **engagement.dict()
    )
    attendee_engagements_db.append(new_engagement)
    return new_engagement

@router.put("/engagements/{engagement_id}", response_model=AttendeeEngagement)
def update_attendee_engagement(engagement_id: int, engagement_update: AttendeeEngagementUpdate):
    """Update an existing attendee engagement"""
    for index, engagement in enumerate(attendee_engagements_db):
        if engagement.id == engagement_id:
            updated_engagement = AttendeeEngagement(
                id=engagement_id,
                **engagement_update.dict()
            )
            attendee_engagements_db[index] = updated_engagement
            return updated_engagement
    raise HTTPException(status_code=404, detail="Attendee engagement not found")

@router.delete("/engagements/{engagement_id}")
def delete_attendee_engagement(engagement_id: int):
    """Delete an attendee engagement"""
    for index, engagement in enumerate(attendee_engagements_db):
        if engagement.id == engagement_id:
            del attendee_engagements_db[index]
            return {"message": "Attendee engagement deleted successfully"}
    raise HTTPException(status_code=404, detail="Attendee engagement not found")

# Post-Event Follow-ups endpoints
@router.get("/follow-ups", response_model=List[PostEventFollowUp])
def list_post_event_follow_ups():
    """List all post-event follow-ups"""
    return post_event_follow_ups_db

@router.get("/follow-ups/{follow_up_id}", response_model=PostEventFollowUp)
def get_post_event_follow_up(follow_up_id: int):
    """Get a specific post-event follow-up by ID"""
    for follow_up in post_event_follow_ups_db:
        if follow_up.id == follow_up_id:
            return follow_up
    raise HTTPException(status_code=404, detail="Post-event follow-up not found")

@router.post("/follow-ups", response_model=PostEventFollowUp)
def create_post_event_follow_up(follow_up: PostEventFollowUpCreate):
    """Create a new post-event follow-up"""
    new_id = max([f.id for f in post_event_follow_ups_db]) + 1 if post_event_follow_ups_db else 1
    new_follow_up = PostEventFollowUp(
        id=new_id,
        created_at=datetime.now(),
        open_count=0,
        click_count=0,
        **follow_up.dict()
    )
    post_event_follow_ups_db.append(new_follow_up)
    return new_follow_up

@router.put("/follow-ups/{follow_up_id}", response_model=PostEventFollowUp)
def update_post_event_follow_up(follow_up_id: int, follow_up_update: PostEventFollowUpUpdate):
    """Update an existing post-event follow-up"""
    for index, follow_up in enumerate(post_event_follow_ups_db):
        if follow_up.id == follow_up_id:
            updated_follow_up = PostEventFollowUp(
                id=follow_up_id,
                created_at=follow_up.created_at,
                updated_at=datetime.now(),
                open_count=follow_up.open_count,
                click_count=follow_up.click_count,
                **follow_up_update.dict()
            )
            post_event_follow_ups_db[index] = updated_follow_up
            return updated_follow_up
    raise HTTPException(status_code=404, detail="Post-event follow-up not found")

@router.delete("/follow-ups/{follow_up_id}")
def delete_post_event_follow_up(follow_up_id: int):
    """Delete a post-event follow-up"""
    for index, follow_up in enumerate(post_event_follow_ups_db):
        if follow_up.id == follow_up_id:
            del post_event_follow_ups_db[index]
            return {"message": "Post-event follow-up deleted successfully"}
    raise HTTPException(status_code=404, detail="Post-event follow-up not found")

@router.post("/follow-ups/{follow_up_id}/send")
def send_post_event_follow_up(follow_up_id: int):
    """Send a post-event follow-up"""
    for index, follow_up in enumerate(post_event_follow_ups_db):
        if follow_up.id == follow_up_id:
            follow_up.is_sent = True
            follow_up.sent_date = datetime.now()
            post_event_follow_ups_db[index] = follow_up
            return {"message": f"Post-event follow-up {follow_up_id} sent"}
    raise HTTPException(status_code=404, detail="Post-event follow-up not found")

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_event_status_options():
    """Get available event statuses"""
    return get_event_statuses()

@router.get("/config/types", response_model=List[str])
def get_event_type_options():
    """Get available event types"""
    return get_event_types()