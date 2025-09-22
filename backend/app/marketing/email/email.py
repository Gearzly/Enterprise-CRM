from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .models import (
    EmailList, EmailListCreate, EmailListUpdate,
    EmailSubscriber, EmailSubscriberCreate, EmailSubscriberUpdate,
    EmailTemplate, EmailTemplateCreate, EmailTemplateUpdate,
    EmailCampaign, EmailCampaignCreate, EmailCampaignUpdate,
    EmailSequence, EmailSequenceCreate, EmailSequenceUpdate,
    EmailSequenceStep, EmailSequenceStepCreate, EmailSequenceStepUpdate
)
from .config import (
    get_email_statuses, get_email_template_categories,
    get_default_open_rate, get_default_click_rate, get_default_bounce_rate
)

router = APIRouter()

# In-memory storage for demo purposes
email_lists_db = []
email_subscribers_db = []
email_templates_db = []
email_campaigns_db = []
email_sequences_db = []
email_sequence_steps_db = []

@router.get("/lists", response_model=List[EmailList])
def list_email_lists():
    """List all email lists"""
    return email_lists_db

@router.get("/lists/{list_id}", response_model=EmailList)
def get_email_list(list_id: int):
    """Get a specific email list by ID"""
    for email_list in email_lists_db:
        if email_list.id == list_id:
            return email_list
    raise HTTPException(status_code=404, detail="Email list not found")

@router.post("/lists", response_model=EmailList)
def create_email_list(email_list: EmailListCreate):
    """Create a new email list"""
    new_id = max([l.id for l in email_lists_db]) + 1 if email_lists_db else 1
    new_email_list = EmailList(
        id=new_id,
        created_at=datetime.now(),
        **email_list.dict()
    )
    email_lists_db.append(new_email_list)
    return new_email_list

@router.put("/lists/{list_id}", response_model=EmailList)
def update_email_list(list_id: int, email_list_update: EmailListUpdate):
    """Update an existing email list"""
    for index, email_list in enumerate(email_lists_db):
        if email_list.id == list_id:
            updated_email_list = EmailList(
                id=list_id,
                created_at=email_list.created_at,
                updated_at=datetime.now(),
                subscriber_count=email_list.subscriber_count,
                **email_list_update.dict()
            )
            email_lists_db[index] = updated_email_list
            return updated_email_list
    raise HTTPException(status_code=404, detail="Email list not found")

@router.delete("/lists/{list_id}")
def delete_email_list(list_id: int):
    """Delete an email list"""
    for index, email_list in enumerate(email_lists_db):
        if email_list.id == list_id:
            del email_lists_db[index]
            return {"message": "Email list deleted successfully"}
    raise HTTPException(status_code=404, detail="Email list not found")

# Email Subscribers endpoints
@router.get("/subscribers", response_model=List[EmailSubscriber])
def list_email_subscribers():
    """List all email subscribers"""
    return email_subscribers_db

@router.get("/subscribers/{subscriber_id}", response_model=EmailSubscriber)
def get_email_subscriber(subscriber_id: int):
    """Get a specific email subscriber by ID"""
    for subscriber in email_subscribers_db:
        if subscriber.id == subscriber_id:
            return subscriber
    raise HTTPException(status_code=404, detail="Email subscriber not found")

@router.post("/subscribers", response_model=EmailSubscriber)
def create_email_subscriber(subscriber: EmailSubscriberCreate):
    """Create a new email subscriber"""
    new_id = max([s.id for s in email_subscribers_db]) + 1 if email_subscribers_db else 1
    new_subscriber = EmailSubscriber(
        id=new_id,
        created_at=datetime.now(),
        **subscriber.dict()
    )
    email_subscribers_db.append(new_subscriber)
    return new_subscriber

@router.put("/subscribers/{subscriber_id}", response_model=EmailSubscriber)
def update_email_subscriber(subscriber_id: int, subscriber_update: EmailSubscriberUpdate):
    """Update an existing email subscriber"""
    for index, subscriber in enumerate(email_subscribers_db):
        if subscriber.id == subscriber_id:
            updated_subscriber = EmailSubscriber(
                id=subscriber_id,
                created_at=subscriber.created_at,
                updated_at=datetime.now(),
                **subscriber_update.dict()
            )
            email_subscribers_db[index] = updated_subscriber
            return updated_subscriber
    raise HTTPException(status_code=404, detail="Email subscriber not found")

@router.delete("/subscribers/{subscriber_id}")
def delete_email_subscriber(subscriber_id: int):
    """Delete an email subscriber"""
    for index, subscriber in enumerate(email_subscribers_db):
        if subscriber.id == subscriber_id:
            del email_subscribers_db[index]
            return {"message": "Email subscriber deleted successfully"}
    raise HTTPException(status_code=404, detail="Email subscriber not found")

@router.post("/subscribers/bulk-import")
def bulk_import_subscribers(subscribers: List[EmailSubscriberCreate]):
    """Bulk import email subscribers"""
    imported_count = 0
    for subscriber_data in subscribers:
        new_id = max([s.id for s in email_subscribers_db]) + 1 if email_subscribers_db else 1
        new_subscriber = EmailSubscriber(
            id=new_id,
            created_at=datetime.now(),
            **subscriber_data.dict()
        )
        email_subscribers_db.append(new_subscriber)
        imported_count += 1
    return {"message": f"Successfully imported {imported_count} subscribers"}

# Email Templates endpoints
@router.get("/templates", response_model=List[EmailTemplate])
def list_email_templates():
    """List all email templates"""
    return email_templates_db

@router.get("/templates/{template_id}", response_model=EmailTemplate)
def get_email_template(template_id: int):
    """Get a specific email template by ID"""
    for template in email_templates_db:
        if template.id == template_id:
            return template
    raise HTTPException(status_code=404, detail="Email template not found")

@router.post("/templates", response_model=EmailTemplate)
def create_email_template(template: EmailTemplateCreate):
    """Create a new email template"""
    new_id = max([t.id for t in email_templates_db]) + 1 if email_templates_db else 1
    new_template = EmailTemplate(
        id=new_id,
        created_at=datetime.now(),
        **template.dict()
    )
    email_templates_db.append(new_template)
    return new_template

@router.put("/templates/{template_id}", response_model=EmailTemplate)
def update_email_template(template_id: int, template_update: EmailTemplateUpdate):
    """Update an existing email template"""
    for index, template in enumerate(email_templates_db):
        if template.id == template_id:
            updated_template = EmailTemplate(
                id=template_id,
                created_at=template.created_at,
                updated_at=datetime.now(),
                **template_update.dict()
            )
            email_templates_db[index] = updated_template
            return updated_template
    raise HTTPException(status_code=404, detail="Email template not found")

@router.delete("/templates/{template_id}")
def delete_email_template(template_id: int):
    """Delete an email template"""
    for index, template in enumerate(email_templates_db):
        if template.id == template_id:
            del email_templates_db[index]
            return {"message": "Email template deleted successfully"}
    raise HTTPException(status_code=404, detail="Email template not found")

# Email Campaigns endpoints
@router.get("/campaigns", response_model=List[EmailCampaign])
def list_email_campaigns():
    """List all email campaigns"""
    return email_campaigns_db

@router.get("/campaigns/{campaign_id}", response_model=EmailCampaign)
def get_email_campaign(campaign_id: int):
    """Get a specific email campaign by ID"""
    for campaign in email_campaigns_db:
        if campaign.id == campaign_id:
            return campaign
    raise HTTPException(status_code=404, detail="Email campaign not found")

@router.post("/campaigns", response_model=EmailCampaign)
def create_email_campaign(campaign: EmailCampaignCreate):
    """Create a new email campaign"""
    new_id = max([c.id for c in email_campaigns_db]) + 1 if email_campaigns_db else 1
    new_campaign = EmailCampaign(
        id=new_id,
        created_at=datetime.now(),
        open_rate=get_default_open_rate(),
        click_rate=get_default_click_rate(),
        bounce_rate=get_default_bounce_rate(),
        **campaign.dict()
    )
    email_campaigns_db.append(new_campaign)
    return new_campaign

@router.put("/campaigns/{campaign_id}", response_model=EmailCampaign)
def update_email_campaign(campaign_id: int, campaign_update: EmailCampaignUpdate):
    """Update an existing email campaign"""
    for index, campaign in enumerate(email_campaigns_db):
        if campaign.id == campaign_id:
            updated_campaign = EmailCampaign(
                id=campaign_id,
                created_at=campaign.created_at,
                updated_at=datetime.now(),
                open_rate=campaign.open_rate,
                click_rate=campaign.click_rate,
                bounce_rate=campaign.bounce_rate,
                unsubscribe_count=campaign.unsubscribe_count,
                **campaign_update.dict()
            )
            email_campaigns_db[index] = updated_campaign
            return updated_campaign
    raise HTTPException(status_code=404, detail="Email campaign not found")

@router.delete("/campaigns/{campaign_id}")
def delete_email_campaign(campaign_id: int):
    """Delete an email campaign"""
    for index, campaign in enumerate(email_campaigns_db):
        if campaign.id == campaign_id:
            del email_campaigns_db[index]
            return {"message": "Email campaign deleted successfully"}
    raise HTTPException(status_code=404, detail="Email campaign not found")

@router.post("/campaigns/{campaign_id}/send")
def send_email_campaign(campaign_id: int):
    """Send an email campaign"""
    for index, campaign in enumerate(email_campaigns_db):
        if campaign.id == campaign_id:
            # Update campaign status to sending
            campaign.status = "Sending"
            campaign.sent_at = datetime.now()
            email_campaigns_db[index] = campaign
            return {"message": f"Email campaign {campaign_id} is being sent"}
    raise HTTPException(status_code=404, detail="Email campaign not found")

@router.get("/campaigns/status/{status}", response_model=List[EmailCampaign])
def get_email_campaigns_by_status(status: str):
    """Get email campaigns by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [campaign for campaign in email_campaigns_db if campaign.status.value == normalized_status]

# Email Sequences endpoints
@router.get("/sequences", response_model=List[EmailSequence])
def list_email_sequences():
    """List all email sequences"""
    return email_sequences_db

@router.get("/sequences/{sequence_id}", response_model=EmailSequence)
def get_email_sequence(sequence_id: int):
    """Get a specific email sequence by ID"""
    for sequence in email_sequences_db:
        if sequence.id == sequence_id:
            return sequence
    raise HTTPException(status_code=404, detail="Email sequence not found")

@router.post("/sequences", response_model=EmailSequence)
def create_email_sequence(sequence: EmailSequenceCreate):
    """Create a new email sequence"""
    new_id = max([s.id for s in email_sequences_db]) + 1 if email_sequences_db else 1
    new_sequence = EmailSequence(
        id=new_id,
        created_at=datetime.now(),
        **sequence.dict()
    )
    email_sequences_db.append(new_sequence)
    return new_sequence

@router.put("/sequences/{sequence_id}", response_model=EmailSequence)
def update_email_sequence(sequence_id: int, sequence_update: EmailSequenceUpdate):
    """Update an existing email sequence"""
    for index, sequence in enumerate(email_sequences_db):
        if sequence.id == sequence_id:
            updated_sequence = EmailSequence(
                id=sequence_id,
                created_at=sequence.created_at,
                updated_at=datetime.now(),
                email_count=sequence.email_count,
                **sequence_update.dict()
            )
            email_sequences_db[index] = updated_sequence
            return updated_sequence
    raise HTTPException(status_code=404, detail="Email sequence not found")

@router.delete("/sequences/{sequence_id}")
def delete_email_sequence(sequence_id: int):
    """Delete an email sequence"""
    for index, sequence in enumerate(email_sequences_db):
        if sequence.id == sequence_id:
            del email_sequences_db[index]
            return {"message": "Email sequence deleted successfully"}
    raise HTTPException(status_code=404, detail="Email sequence not found")

# Email Sequence Steps endpoints
@router.get("/sequence-steps", response_model=List[EmailSequenceStep])
def list_email_sequence_steps():
    """List all email sequence steps"""
    return email_sequence_steps_db

@router.get("/sequence-steps/{step_id}", response_model=EmailSequenceStep)
def get_email_sequence_step(step_id: int):
    """Get a specific email sequence step by ID"""
    for step in email_sequence_steps_db:
        if step.id == step_id:
            return step
    raise HTTPException(status_code=404, detail="Email sequence step not found")

@router.post("/sequence-steps", response_model=EmailSequenceStep)
def create_email_sequence_step(step: EmailSequenceStepCreate):
    """Create a new email sequence step"""
    new_id = max([s.id for s in email_sequence_steps_db]) + 1 if email_sequence_steps_db else 1
    new_step = EmailSequenceStep(
        id=new_id,
        created_at=datetime.now(),
        **step.dict()
    )
    email_sequence_steps_db.append(new_step)
    return new_step

@router.put("/sequence-steps/{step_id}", response_model=EmailSequenceStep)
def update_email_sequence_step(step_id: int, step_update: EmailSequenceStepUpdate):
    """Update an existing email sequence step"""
    for index, step in enumerate(email_sequence_steps_db):
        if step.id == step_id:
            updated_step = EmailSequenceStep(
                id=step_id,
                created_at=step.created_at,
                updated_at=datetime.now(),
                **step_update.dict()
            )
            email_sequence_steps_db[index] = updated_step
            return updated_step
    raise HTTPException(status_code=404, detail="Email sequence step not found")

@router.delete("/sequence-steps/{step_id}")
def delete_email_sequence_step(step_id: int):
    """Delete an email sequence step"""
    for index, step in enumerate(email_sequence_steps_db):
        if step.id == step_id:
            del email_sequence_steps_db[index]
            return {"message": "Email sequence step deleted successfully"}
    raise HTTPException(status_code=404, detail="Email sequence step not found")

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_email_status_options():
    """Get available email status options"""
    return get_email_statuses()

@router.get("/config/template-categories", response_model=List[str])
def get_email_template_category_options():
    """Get available email template categories"""
    return get_email_template_categories()