from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
from app.core.database import Base

class Campaign(Base):
    __tablename__ = "marketing_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    type = Column(String)
    status = Column(String, default="Draft")
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True), nullable=True)
    budget = Column(Float, nullable=True)
    assigned_to = Column(String, nullable=True)
    tags = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CampaignTemplate(Base):
    __tablename__ = "marketing_campaign_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    type = Column(String)
    content = Column(Text)  # JSON template content
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Lead(Base):
    __tablename__ = "marketing_leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    status = Column(String, default="New")
    source = Column(String, default="Website")
    assigned_to = Column(String, nullable=True)
    value = Column(Float, nullable=True)
    score = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LeadForm(Base):
    __tablename__ = "marketing_lead_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    fields = Column(Text)  # JSON structure for form fields
    is_active = Column(Boolean, default=True)
    redirect_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LeadScoreRule(Base):
    __tablename__ = "marketing_lead_score_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    rule_type = Column(String)
    criteria = Column(Text)  # JSON structure for scoring criteria
    points = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LeadAssignmentRule(Base):
    __tablename__ = "marketing_lead_assignment_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    criteria = Column(Text)  # JSON structure for assignment criteria
    assign_to = Column(String)  # User or team to assign to
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ABTest(Base):
    __tablename__ = "marketing_ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    campaign_id = Column(Integer)
    variant_a_content = Column(Text)
    variant_b_content = Column(Text)
    test_metric = Column(String)  # e.g., "click_rate", "conversion_rate"
    status = Column(String, default="draft")  # draft, running, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Email Marketing Models
class EmailList(Base):
    __tablename__ = "marketing_email_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    tags = Column(Text, nullable=True)  # JSON string
    subscriber_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmailSubscriber(Base):
    __tablename__ = "marketing_email_subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    list_ids = Column(Text)  # JSON string of list IDs
    tags = Column(Text, nullable=True)  # JSON string
    is_subscribed = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmailTemplate(Base):
    __tablename__ = "marketing_email_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    content = Column(Text)  # HTML content
    category = Column(String, default="Newsletter")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmailCampaign(Base):
    __tablename__ = "marketing_email_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    template_id = Column(Integer)
    list_ids = Column(Text)  # JSON string of list IDs
    status = Column(String, default="Draft")
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    unsubscribe_count = Column(Integer, default=0)
    tags = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmailSequence(Base):
    __tablename__ = "marketing_email_sequences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    tags = Column(Text, nullable=True)  # JSON string
    email_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EmailSequenceStep(Base):
    __tablename__ = "marketing_email_sequence_steps"

    id = Column(Integer, primary_key=True, index=True)
    sequence_id = Column(Integer)
    email_template_id = Column(Integer)
    delay_days = Column(Integer)
    step_order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())