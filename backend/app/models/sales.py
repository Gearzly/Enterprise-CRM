from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
from app.core.database import Base
from app.core.config.dynamic_config import get_sales_default

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    status = Column(String, default=lambda: get_sales_default("lead_status"))
    source = Column(String, default=lambda: get_sales_default("lead_source"))
    assigned_to = Column(String, nullable=True)
    value = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, index=True)
    position = Column(String, nullable=True)
    department = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    contact_type = Column(String, default=lambda: get_sales_default("contact_type"))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    value = Column(Float)
    stage = Column(String, default=lambda: get_sales_default("opportunity_stage"))
    probability = Column(Integer, default=0)  # Percentage
    close_date = Column(DateTime(timezone=True), nullable=True)
    account_id = Column(Integer)
    contact_id = Column(Integer)
    assigned_to = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    opportunity_id = Column(Integer)
    account_id = Column(Integer)
    contact_id = Column(Integer)
    amount = Column(Float)
    tax_amount = Column(Float, default=lambda: get_sales_default("default_tax_rate"))
    total_amount = Column(Float)
    status = Column(String, default=lambda: get_sales_default("quotation_status"))
    valid_until = Column(DateTime(timezone=True))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    activity_type = Column(String)
    status = Column(String, default=lambda: get_sales_default("activity_status"))
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    related_to = Column(String, nullable=True)  # Could be lead, contact, opportunity, etc.
    related_id = Column(Integer, nullable=True)
    assigned_to = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    target_type = Column(String)
    period = Column(String)
    year = Column(Integer)
    target_value = Column(Float)
    assigned_to = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    report_type = Column(String)
    status = Column(String, default=lambda: get_sales_default("report_status"))
    generated_by = Column(String, nullable=True)
    filters = Column(Text, nullable=True)  # JSON string
    data = Column(Text, nullable=True)  # JSON string
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    generated_at = Column(DateTime(timezone=True), nullable=True)