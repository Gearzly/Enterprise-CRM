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
    priority = Column(String)
    response_time_hours = Column(Integer)  # Hours to respond
    resolution_time_hours = Column(Integer)  # Hours to resolve
    is_active = Column(Boolean, default=lambda: get_support_default("sla_status") == "Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())