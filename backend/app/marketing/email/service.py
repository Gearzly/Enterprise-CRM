from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.marketing import (
    EmailList as DBEmailList,
    EmailSubscriber as DBEmailSubscriber,
    EmailTemplate as DBEmailTemplate,
    EmailCampaign as DBEmailCampaign,
    EmailSequence as DBEmailSequence,
    EmailSequenceStep as DBEmailSequenceStep
)
from app.marketing.email.models import (
    EmailListCreate, EmailListUpdate,
    EmailSubscriberCreate, EmailSubscriberUpdate,
    EmailTemplateCreate, EmailTemplateUpdate,
    EmailCampaignCreate, EmailCampaignUpdate,
    EmailSequenceCreate, EmailSequenceUpdate,
    EmailSequenceStepCreate, EmailSequenceStepUpdate
)
import json


class EmailService:
    """Service class for handling email marketing operations"""

    def get_email_lists(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailList]:
        """Get all email lists"""
        return db.query(DBEmailList).offset(skip).limit(limit).all()

    def get_email_list(self, db: Session, list_id: int) -> Optional[DBEmailList]:
        """Get a specific email list by ID"""
        return db.query(DBEmailList).filter(DBEmailList.id == list_id).first()

    def create_email_list(self, db: Session, email_list: EmailListCreate) -> DBEmailList:
        """Create a new email list"""
        db_email_list = DBEmailList(
            name=email_list.name,
            description=email_list.description,
            is_active=email_list.is_active,
            tags=json.dumps(email_list.tags) if email_list.tags else None,
            subscriber_count=0
        )
        db.add(db_email_list)
        db.commit()
        db.refresh(db_email_list)
        return db_email_list

    def update_email_list(self, db: Session, list_id: int, email_list_update: EmailListUpdate) -> Optional[DBEmailList]:
        """Update an existing email list"""
        db_email_list = db.query(DBEmailList).filter(DBEmailList.id == list_id).first()
        if db_email_list:
            update_data = email_list_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key == "tags":
                    setattr(db_email_list, key, json.dumps(value) if value else None)
                else:
                    setattr(db_email_list, key, value)
            db.commit()
            db.refresh(db_email_list)
        return db_email_list

    def delete_email_list(self, db: Session, list_id: int) -> bool:
        """Delete an email list"""
        db_email_list = db.query(DBEmailList).filter(DBEmailList.id == list_id).first()
        if db_email_list:
            db.delete(db_email_list)
            db.commit()
            return True
        return False

    def get_email_subscribers(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailSubscriber]:
        """Get all email subscribers"""
        return db.query(DBEmailSubscriber).offset(skip).limit(limit).all()

    def get_email_subscriber(self, db: Session, subscriber_id: int) -> Optional[DBEmailSubscriber]:
        """Get a specific email subscriber by ID"""
        return db.query(DBEmailSubscriber).filter(DBEmailSubscriber.id == subscriber_id).first()

    def create_email_subscriber(self, db: Session, subscriber: EmailSubscriberCreate) -> DBEmailSubscriber:
        """Create a new email subscriber"""
        db_subscriber = DBEmailSubscriber(
            email=subscriber.email,
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
            list_ids=json.dumps(subscriber.list_ids) if subscriber.list_ids else None,
            tags=json.dumps(subscriber.tags) if subscriber.tags else None,
            is_subscribed=subscriber.is_subscribed
        )
        db.add(db_subscriber)
        db.commit()
        db.refresh(db_subscriber)
        return db_subscriber

    def update_email_subscriber(self, db: Session, subscriber_id: int, subscriber_update: EmailSubscriberUpdate) -> Optional[DBEmailSubscriber]:
        """Update an existing email subscriber"""
        db_subscriber = db.query(DBEmailSubscriber).filter(DBEmailSubscriber.id == subscriber_id).first()
        if db_subscriber:
            update_data = subscriber_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key in ["list_ids", "tags"]:
                    setattr(db_subscriber, key, json.dumps(value) if value else None)
                else:
                    setattr(db_subscriber, key, value)
            db.commit()
            db.refresh(db_subscriber)
        return db_subscriber

    def delete_email_subscriber(self, db: Session, subscriber_id: int) -> bool:
        """Delete an email subscriber"""
        db_subscriber = db.query(DBEmailSubscriber).filter(DBEmailSubscriber.id == subscriber_id).first()
        if db_subscriber:
            db.delete(db_subscriber)
            db.commit()
            return True
        return False

    def bulk_import_subscribers(self, db: Session, subscribers: List[EmailSubscriberCreate]) -> int:
        """Bulk import email subscribers"""
        imported_count = 0
        for subscriber_data in subscribers:
            db_subscriber = DBEmailSubscriber(
                email=subscriber_data.email,
                first_name=subscriber_data.first_name,
                last_name=subscriber_data.last_name,
                list_ids=json.dumps(subscriber_data.list_ids) if subscriber_data.list_ids else None,
                tags=json.dumps(subscriber_data.tags) if subscriber_data.tags else None,
                is_subscribed=subscriber_data.is_subscribed
            )
            db.add(db_subscriber)
            imported_count += 1
        db.commit()
        return imported_count

    def get_email_templates(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailTemplate]:
        """Get all email templates"""
        return db.query(DBEmailTemplate).offset(skip).limit(limit).all()

    def get_email_template(self, db: Session, template_id: int) -> Optional[DBEmailTemplate]:
        """Get a specific email template by ID"""
        return db.query(DBEmailTemplate).filter(DBEmailTemplate.id == template_id).first()

    def create_email_template(self, db: Session, template: EmailTemplateCreate) -> DBEmailTemplate:
        """Create a new email template"""
        db_template = DBEmailTemplate(
            name=template.name,
            subject=template.subject,
            content=template.content,
            category=template.category,
            is_active=template.is_active
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template

    def update_email_template(self, db: Session, template_id: int, template_update: EmailTemplateUpdate) -> Optional[DBEmailTemplate]:
        """Update an existing email template"""
        db_template = db.query(DBEmailTemplate).filter(DBEmailTemplate.id == template_id).first()
        if db_template:
            update_data = template_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_template, key, value)
            db.commit()
            db.refresh(db_template)
        return db_template

    def delete_email_template(self, db: Session, template_id: int) -> bool:
        """Delete an email template"""
        db_template = db.query(DBEmailTemplate).filter(DBEmailTemplate.id == template_id).first()
        if db_template:
            db.delete(db_template)
            db.commit()
            return True
        return False

    def get_email_campaigns(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailCampaign]:
        """Get all email campaigns"""
        return db.query(DBEmailCampaign).offset(skip).limit(limit).all()

    def get_email_campaign(self, db: Session, campaign_id: int) -> Optional[DBEmailCampaign]:
        """Get a specific email campaign by ID"""
        return db.query(DBEmailCampaign).filter(DBEmailCampaign.id == campaign_id).first()

    def create_email_campaign(self, db: Session, campaign: EmailCampaignCreate, 
                             default_open_rate: float = 0.0, 
                             default_click_rate: float = 0.0, 
                             default_bounce_rate: float = 0.0) -> DBEmailCampaign:
        """Create a new email campaign"""
        db_campaign = DBEmailCampaign(
            name=campaign.name,
            subject=campaign.subject,
            template_id=campaign.template_id,
            list_ids=json.dumps(campaign.list_ids) if campaign.list_ids else None,
            status=campaign.status,
            scheduled_at=campaign.scheduled_at,
            sent_at=campaign.sent_at,
            open_rate=default_open_rate,
            click_rate=default_click_rate,
            bounce_rate=default_bounce_rate,
            unsubscribe_count=0,
            tags=json.dumps(campaign.tags) if campaign.tags else None
        )
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign

    def update_email_campaign(self, db: Session, campaign_id: int, campaign_update: EmailCampaignUpdate) -> Optional[DBEmailCampaign]:
        """Update an existing email campaign"""
        db_campaign = db.query(DBEmailCampaign).filter(DBEmailCampaign.id == campaign_id).first()
        if db_campaign:
            update_data = campaign_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key in ["list_ids", "tags"]:
                    setattr(db_campaign, key, json.dumps(value) if value else None)
                else:
                    setattr(db_campaign, key, value)
            db.commit()
            db.refresh(db_campaign)
        return db_campaign

    def delete_email_campaign(self, db: Session, campaign_id: int) -> bool:
        """Delete an email campaign"""
        db_campaign = db.query(DBEmailCampaign).filter(DBEmailCampaign.id == campaign_id).first()
        if db_campaign:
            db.delete(db_campaign)
            db.commit()
            return True
        return False

    def send_email_campaign(self, db: Session, campaign_id: int) -> Optional[DBEmailCampaign]:
        """Send an email campaign"""
        db_campaign = db.query(DBEmailCampaign).filter(DBEmailCampaign.id == campaign_id).first()
        if db_campaign:
            update_data = {
                "status": "Sending",
                "sent_at": datetime.now()
            }
            for field, value in update_data.items():
                setattr(db_campaign, field, value)
            db.commit()
            db.refresh(db_campaign)
        return db_campaign

    def get_email_campaigns_by_status(self, db: Session, status: str) -> List[DBEmailCampaign]:
        """Get email campaigns by status"""
        # Normalize the status parameter to handle case differences
        normalized_status = status.lower().title()
        return db.query(DBEmailCampaign).filter(DBEmailCampaign.status == normalized_status).all()

    def get_email_sequences(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailSequence]:
        """Get all email sequences"""
        return db.query(DBEmailSequence).offset(skip).limit(limit).all()

    def get_email_sequence(self, db: Session, sequence_id: int) -> Optional[DBEmailSequence]:
        """Get a specific email sequence by ID"""
        return db.query(DBEmailSequence).filter(DBEmailSequence.id == sequence_id).first()

    def create_email_sequence(self, db: Session, sequence: EmailSequenceCreate) -> DBEmailSequence:
        """Create a new email sequence"""
        db_sequence = DBEmailSequence(
            name=sequence.name,
            description=sequence.description,
            is_active=sequence.is_active,
            tags=json.dumps(sequence.tags) if sequence.tags else None,
            email_count=0
        )
        db.add(db_sequence)
        db.commit()
        db.refresh(db_sequence)
        return db_sequence

    def update_email_sequence(self, db: Session, sequence_id: int, sequence_update: EmailSequenceUpdate) -> Optional[DBEmailSequence]:
        """Update an existing email sequence"""
        db_sequence = db.query(DBEmailSequence).filter(DBEmailSequence.id == sequence_id).first()
        if db_sequence:
            update_data = sequence_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key == "tags":
                    setattr(db_sequence, key, json.dumps(value) if value else None)
                else:
                    setattr(db_sequence, key, value)
            db.commit()
            db.refresh(db_sequence)
        return db_sequence

    def delete_email_sequence(self, db: Session, sequence_id: int) -> bool:
        """Delete an email sequence"""
        db_sequence = db.query(DBEmailSequence).filter(DBEmailSequence.id == sequence_id).first()
        if db_sequence:
            db.delete(db_sequence)
            db.commit()
            return True
        return False

    def get_email_sequence_steps(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBEmailSequenceStep]:
        """Get all email sequence steps"""
        return db.query(DBEmailSequenceStep).offset(skip).limit(limit).all()

    def get_email_sequence_step(self, db: Session, step_id: int) -> Optional[DBEmailSequenceStep]:
        """Get a specific email sequence step by ID"""
        return db.query(DBEmailSequenceStep).filter(DBEmailSequenceStep.id == step_id).first()

    def create_email_sequence_step(self, db: Session, step: EmailSequenceStepCreate) -> DBEmailSequenceStep:
        """Create a new email sequence step"""
        db_step = DBEmailSequenceStep(
            sequence_id=step.sequence_id,
            email_template_id=step.email_template_id,
            delay_days=step.delay_days,
            step_order=step.step_order
        )
        db.add(db_step)
        db.commit()
        db.refresh(db_step)
        return db_step

    def update_email_sequence_step(self, db: Session, step_id: int, step_update: EmailSequenceStepUpdate) -> Optional[DBEmailSequenceStep]:
        """Update an existing email sequence step"""
        db_step = db.query(DBEmailSequenceStep).filter(DBEmailSequenceStep.id == step_id).first()
        if db_step:
            update_data = step_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_step, key, value)
            db.commit()
            db.refresh(db_step)
        return db_step

    def delete_email_sequence_step(self, db: Session, step_id: int) -> bool:
        """Delete an email sequence step"""
        db_step = db.query(DBEmailSequenceStep).filter(DBEmailSequenceStep.id == step_id).first()
        if db_step:
            db.delete(db_step)
            db.commit()
            return True
        return False