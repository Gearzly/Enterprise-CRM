from enum import Enum

class LeadStatus(str, Enum):
    new = "New"
    contacted = "Contacted"
    qualified = "Qualified"
    unqualified = "Unqualified"
    converted = "Converted"

class LeadSource(str, Enum):
    website = "Website"
    referral = "Referral"
    social_media = "Social Media"
    email_campaign = "Email Campaign"
    event = "Event"
    other = "Other"

class OpportunityStage(str, Enum):
    prospecting = "Prospecting"
    qualification = "Qualification"
    proposal = "Proposal"
    negotiation = "Negotiation"
    closed_won = "Closed Won"
    closed_lost = "Closed Lost"

class QuotationStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    viewed = "Viewed"
    accepted = "Accepted"
    rejected = "Rejected"
    expired = "Expired"

class ContactType(str, Enum):
    primary = "Primary"
    secondary = "Secondary"
    billing = "Billing"
    shipping = "Shipping"

class ActivityType(str, Enum):
    call = "Call"
    meeting = "Meeting"
    email = "Email"
    task = "Task"
    note = "Note"

class ActivityStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"
    cancelled = "Cancelled"

class TargetPeriod(str, Enum):
    monthly = "Monthly"
    quarterly = "Quarterly"
    yearly = "Yearly"

class TargetType(str, Enum):
    revenue = "Revenue"
    leads = "Leads"
    opportunities = "Opportunities"
    conversions = "Conversions"

class ReportType(str, Enum):
    sales_performance = "Sales Performance"
    pipeline_analysis = "Pipeline Analysis"
    revenue_forecast = "Revenue Forecast"
    activity_summary = "Activity Summary"
    quota_attainment = "Quota Attainment"

class ReportStatus(str, Enum):
    draft = "Draft"
    generated = "Generated"
    published = "Published"
    archived = "Archived"