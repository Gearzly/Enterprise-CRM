from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PartnerStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"
    pending = "Pending"
    suspended = "Suspended"

class PartnerType(str, Enum):
    reseller = "Reseller"
    distributor = "Distributor"
    affiliate = "Affiliate"
    technology = "Technology Partner"
    strategic = "Strategic Partner"
    other = "Other"

class PartnerBase(BaseModel):
    name: str
    company_name: str
    contact_person: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    partner_type: PartnerType
    status: PartnerStatus = PartnerStatus.pending
    commission_rate: Optional[float] = None
    notes: Optional[str] = None

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(PartnerBase):
    pass

class Partner(PartnerBase):
    id: int
    referral_count: int = 0
    conversion_rate: float = 0.0
    total_commission: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class ReferralBase(BaseModel):
    partner_id: int
    referred_by: str  # Name of the partner
    referred_contact_name: str
    referred_contact_email: str
    referred_contact_phone: Optional[str] = None
    status: str = "New"  # New, Contacted, Qualified, Converted, Lost
    conversion_date: Optional[datetime] = None
    commission_earned: Optional[float] = None

class ReferralCreate(ReferralBase):
    pass

class ReferralUpdate(ReferralBase):
    pass

class Referral(ReferralBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class AffiliateProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    commission_structure: Dict[str, Any]  # JSON structure for commission rules
    is_active: bool = True
    terms_and_conditions: Optional[str] = None

class AffiliateProgramCreate(AffiliateProgramBase):
    pass

class AffiliateProgramUpdate(AffiliateProgramBase):
    pass

class AffiliateProgram(AffiliateProgramBase):
    id: int
    affiliate_count: int = 0
    total_payout: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class CoMarketingCampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    partner_id: int
    start_date: datetime
    end_date: datetime
    budget: Optional[float] = None
    status: str = "Planned"  # Planned, Active, Completed, Cancelled
    objectives: List[str] = []
    results: Optional[str] = None

class CoMarketingCampaignCreate(CoMarketingCampaignBase):
    pass

class CoMarketingCampaignUpdate(CoMarketingCampaignBase):
    pass

class CoMarketingCampaign(CoMarketingCampaignBase):
    id: int
    roi: float = 0.0
    revenue_generated: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

class PartnerPerformanceBase(BaseModel):
    partner_id: int
    period_start: datetime
    period_end: datetime
    revenue_generated: float = 0.0
    leads_generated: int = 0
    conversions: int = 0
    commission_paid: float = 0.0
    satisfaction_score: Optional[float] = None

class PartnerPerformanceCreate(PartnerPerformanceBase):
    pass

class PartnerPerformanceUpdate(PartnerPerformanceBase):
    pass

class PartnerPerformance(PartnerPerformanceBase):
    id: int
    created_at: datetime