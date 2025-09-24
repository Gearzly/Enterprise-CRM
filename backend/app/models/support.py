from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
from app.core.database import Base
from app.core.config.dynamic_config import get_support_default

class Ticket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    description = Column(Text)
    customer_id = Column(Integer)
    customer_email = Column(String, index=True)
    priority = Column(String, default=lambda: get_support_default("ticket_priority"))
    status = Column(String, default=lambda: get_support_default("ticket_status"))
    channel = Column(String, default=lambda: get_support_default("ticket_channel"))
    assigned_to = Column(String, nullable=True)
    tags = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

class SLA(Base):
    __tablename__ = "support_slas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    type = Column(String, default=lambda: get_support_default("sla_type"))
    priority = Column(String)
    response_time_hours = Column(Integer)  # Hours to respond
    resolution_time_hours = Column(Integer)  # Hours to resolve
    is_active = Column(Boolean, default=lambda: get_support_default("sla_status") == "Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SLABreach(Base):
    __tablename__ = "support_sla_breaches"

    id = Column(Integer, primary_key=True, index=True)
    sla_id = Column(Integer, index=True)
    ticket_id = Column(Integer, index=True)
    breach_reason = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class SLANotification(Base):
    __tablename__ = "support_sla_notifications"

    id = Column(Integer, primary_key=True, index=True)
    sla_id = Column(Integer, index=True)
    threshold_percentage = Column(Integer)  # Percentage of SLA time elapsed before notification
    notification_type = Column(String)  # email, sms, in_app
    recipient_type = Column(String)  # customer, agent, team
    message_template = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())