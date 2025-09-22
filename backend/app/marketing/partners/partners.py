from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from .models import (
    Partner, PartnerCreate, PartnerUpdate,
    Referral, ReferralCreate, ReferralUpdate,
    AffiliateProgram, AffiliateProgramCreate, AffiliateProgramUpdate,
    CoMarketingCampaign, CoMarketingCampaignCreate, CoMarketingCampaignUpdate,
    PartnerPerformance, PartnerPerformanceCreate, PartnerPerformanceUpdate
)
from .config import (
    get_partner_statuses, get_partner_types,
    get_default_commission_rate, get_default_conversion_rate
)

router = APIRouter()

# In-memory storage for demo purposes
partners_db = []
referrals_db = []
affiliate_programs_db = []
co_marketing_campaigns_db = []
partner_performances_db = []

@router.get("/partners", response_model=List[Partner])
def list_partners():
    """List all partners"""
    return partners_db

@router.get("/partners/{partner_id}", response_model=Partner)
def get_partner(partner_id: int):
    """Get a specific partner by ID"""
    for partner in partners_db:
        if partner.id == partner_id:
            return partner
    raise HTTPException(status_code=404, detail="Partner not found")

@router.post("/partners", response_model=Partner)
def create_partner(partner: PartnerCreate):
    """Create a new partner"""
    new_id = max([p.id for p in partners_db]) + 1 if partners_db else 1
    new_partner = Partner(
        id=new_id,
        created_at=datetime.now(),
        referral_count=0,
        conversion_rate=get_default_conversion_rate(),
        total_commission=0.0,
        **partner.dict()
    )
    partners_db.append(new_partner)
    return new_partner

@router.put("/partners/{partner_id}", response_model=Partner)
def update_partner(partner_id: int, partner_update: PartnerUpdate):
    """Update an existing partner"""
    for index, partner in enumerate(partners_db):
        if partner.id == partner_id:
            updated_partner = Partner(
                id=partner_id,
                created_at=partner.created_at,
                updated_at=datetime.now(),
                referral_count=partner.referral_count,
                conversion_rate=partner.conversion_rate,
                total_commission=partner.total_commission,
                **partner_update.dict()
            )
            partners_db[index] = updated_partner
            return updated_partner
    raise HTTPException(status_code=404, detail="Partner not found")

@router.delete("/partners/{partner_id}")
def delete_partner(partner_id: int):
    """Delete a partner"""
    for index, partner in enumerate(partners_db):
        if partner.id == partner_id:
            del partners_db[index]
            return {"message": "Partner deleted successfully"}
    raise HTTPException(status_code=404, detail="Partner not found")

@router.get("/partners/status/{status}", response_model=List[Partner])
def get_partners_by_status(status: str):
    """Get partners by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [partner for partner in partners_db if partner.status.value == normalized_status]

@router.get("/partners/type/{partner_type}", response_model=List[Partner])
def get_partners_by_type(partner_type: str):
    """Get partners by type"""
    # Normalize the partner_type parameter to handle case differences
    normalized_type = partner_type.lower().title()
    return [partner for partner in partners_db if partner.partner_type.value == normalized_type]

@router.post("/partners/{partner_id}/activate")
def activate_partner(partner_id: int):
    """Activate a partner"""
    for index, partner in enumerate(partners_db):
        if partner.id == partner_id:
            partner.status = "Active"
            partners_db[index] = partner
            return {"message": f"Partner {partner_id} activated"}
    raise HTTPException(status_code=404, detail="Partner not found")

@router.post("/partners/{partner_id}/suspend")
def suspend_partner(partner_id: int):
    """Suspend a partner"""
    for index, partner in enumerate(partners_db):
        if partner.id == partner_id:
            partner.status = "Suspended"
            partners_db[index] = partner
            return {"message": f"Partner {partner_id} suspended"}
    raise HTTPException(status_code=404, detail="Partner not found")

# Referrals endpoints
@router.get("/referrals", response_model=List[Referral])
def list_referrals():
    """List all referrals"""
    return referrals_db

@router.get("/referrals/{referral_id}", response_model=Referral)
def get_referral(referral_id: int):
    """Get a specific referral by ID"""
    for referral in referrals_db:
        if referral.id == referral_id:
            return referral
    raise HTTPException(status_code=404, detail="Referral not found")

@router.post("/referrals", response_model=Referral)
def create_referral(referral: ReferralCreate):
    """Create a new referral"""
    new_id = max([r.id for r in referrals_db]) + 1 if referrals_db else 1
    new_referral = Referral(
        id=new_id,
        created_at=datetime.now(),
        **referral.dict()
    )
    referrals_db.append(new_referral)
    
    # Update partner referral count
    for partner in partners_db:
        if partner.id == referral.partner_id:
            partner.referral_count += 1
            break
    
    return new_referral

@router.put("/referrals/{referral_id}", response_model=Referral)
def update_referral(referral_id: int, referral_update: ReferralUpdate):
    """Update an existing referral"""
    for index, referral in enumerate(referrals_db):
        if referral.id == referral_id:
            updated_referral = Referral(
                id=referral_id,
                created_at=referral.created_at,
                updated_at=datetime.now(),
                **referral_update.dict()
            )
            referrals_db[index] = updated_referral
            return updated_referral
    raise HTTPException(status_code=404, detail="Referral not found")

@router.delete("/referrals/{referral_id}")
def delete_referral(referral_id: int):
    """Delete a referral"""
    for index, referral in enumerate(referrals_db):
        if referral.id == referral_id:
            del referrals_db[index]
            return {"message": "Referral deleted successfully"}
    raise HTTPException(status_code=404, detail="Referral not found")

@router.post("/referrals/{referral_id}/convert")
def convert_referral(referral_id: int, commission_amount: float):
    """Convert a referral and record commission"""
    for index, referral in enumerate(referrals_db):
        if referral.id == referral_id:
            referral.status = "Converted"
            referral.conversion_date = datetime.now()
            referral.commission_earned = commission_amount
            referrals_db[index] = referral
            
            # Update partner metrics
            for partner in partners_db:
                if partner.id == referral.partner_id:
                    partner.total_commission += commission_amount
                    # Recalculate conversion rate
                    converted_referrals = len([r for r in referrals_db if r.partner_id == partner.id and r.status == "Converted"])
                    total_referrals = partner.referral_count
                    partner.conversion_rate = converted_referrals / total_referrals if total_referrals > 0 else 0.0
                    break
                    
            return {"message": f"Referral {referral_id} converted"}
    raise HTTPException(status_code=404, detail="Referral not found")

@router.get("/referrals/partner/{partner_id}", response_model=List[Referral])
def get_referrals_by_partner(partner_id: int):
    """Get referrals by partner ID"""
    return [referral for referral in referrals_db if referral.partner_id == partner_id]

# Affiliate Programs endpoints
@router.get("/affiliate-programs", response_model=List[AffiliateProgram])
def list_affiliate_programs():
    """List all affiliate programs"""
    return affiliate_programs_db

@router.get("/affiliate-programs/{program_id}", response_model=AffiliateProgram)
def get_affiliate_program(program_id: int):
    """Get a specific affiliate program by ID"""
    for program in affiliate_programs_db:
        if program.id == program_id:
            return program
    raise HTTPException(status_code=404, detail="Affiliate program not found")

@router.post("/affiliate-programs", response_model=AffiliateProgram)
def create_affiliate_program(program: AffiliateProgramCreate):
    """Create a new affiliate program"""
    new_id = max([p.id for p in affiliate_programs_db]) + 1 if affiliate_programs_db else 1
    new_program = AffiliateProgram(
        id=new_id,
        created_at=datetime.now(),
        affiliate_count=0,
        total_payout=0.0,
        **program.dict()
    )
    affiliate_programs_db.append(new_program)
    return new_program

@router.put("/affiliate-programs/{program_id}", response_model=AffiliateProgram)
def update_affiliate_program(program_id: int, program_update: AffiliateProgramUpdate):
    """Update an existing affiliate program"""
    for index, program in enumerate(affiliate_programs_db):
        if program.id == program_id:
            updated_program = AffiliateProgram(
                id=program_id,
                created_at=program.created_at,
                updated_at=datetime.now(),
                affiliate_count=program.affiliate_count,
                total_payout=program.total_payout,
                **program_update.dict()
            )
            affiliate_programs_db[index] = updated_program
            return updated_program
    raise HTTPException(status_code=404, detail="Affiliate program not found")

@router.delete("/affiliate-programs/{program_id}")
def delete_affiliate_program(program_id: int):
    """Delete an affiliate program"""
    for index, program in enumerate(affiliate_programs_db):
        if program.id == program_id:
            del affiliate_programs_db[index]
            return {"message": "Affiliate program deleted successfully"}
    raise HTTPException(status_code=404, detail="Affiliate program not found")

# Co-Marketing Campaigns endpoints
@router.get("/co-marketing-campaigns", response_model=List[CoMarketingCampaign])
def list_co_marketing_campaigns():
    """List all co-marketing campaigns"""
    return co_marketing_campaigns_db

@router.get("/co-marketing-campaigns/{campaign_id}", response_model=CoMarketingCampaign)
def get_co_marketing_campaign(campaign_id: int):
    """Get a specific co-marketing campaign by ID"""
    for campaign in co_marketing_campaigns_db:
        if campaign.id == campaign_id:
            return campaign
    raise HTTPException(status_code=404, detail="Co-marketing campaign not found")

@router.post("/co-marketing-campaigns", response_model=CoMarketingCampaign)
def create_co_marketing_campaign(campaign: CoMarketingCampaignCreate):
    """Create a new co-marketing campaign"""
    new_id = max([c.id for c in co_marketing_campaigns_db]) + 1 if co_marketing_campaigns_db else 1
    new_campaign = CoMarketingCampaign(
        id=new_id,
        created_at=datetime.now(),
        roi=0.0,
        revenue_generated=0.0,
        **campaign.dict()
    )
    co_marketing_campaigns_db.append(new_campaign)
    return new_campaign

@router.put("/co-marketing-campaigns/{campaign_id}", response_model=CoMarketingCampaign)
def update_co_marketing_campaign(campaign_id: int, campaign_update: CoMarketingCampaignUpdate):
    """Update an existing co-marketing campaign"""
    for index, campaign in enumerate(co_marketing_campaigns_db):
        if campaign.id == campaign_id:
            updated_campaign = CoMarketingCampaign(
                id=campaign_id,
                created_at=campaign.created_at,
                updated_at=datetime.now(),
                roi=campaign.roi,
                revenue_generated=campaign.revenue_generated,
                **campaign_update.dict()
            )
            co_marketing_campaigns_db[index] = updated_campaign
            return updated_campaign
    raise HTTPException(status_code=404, detail="Co-marketing campaign not found")

@router.delete("/co-marketing-campaigns/{campaign_id}")
def delete_co_marketing_campaign(campaign_id: int):
    """Delete a co-marketing campaign"""
    for index, campaign in enumerate(co_marketing_campaigns_db):
        if campaign.id == campaign_id:
            del co_marketing_campaigns_db[index]
            return {"message": "Co-marketing campaign deleted successfully"}
    raise HTTPException(status_code=404, detail="Co-marketing campaign not found")

@router.post("/co-marketing-campaigns/{campaign_id}/complete")
def complete_co_marketing_campaign(campaign_id: int, revenue: float, roi: float):
    """Complete a co-marketing campaign and record results"""
    for index, campaign in enumerate(co_marketing_campaigns_db):
        if campaign.id == campaign_id:
            campaign.status = "Completed"
            campaign.revenue_generated = revenue
            campaign.roi = roi
            campaign.updated_at = datetime.now()
            co_marketing_campaigns_db[index] = campaign
            return {"message": f"Co-marketing campaign {campaign_id} completed"}
    raise HTTPException(status_code=404, detail="Co-marketing campaign not found")

# Partner Performance endpoints
@router.get("/performance", response_model=List[PartnerPerformance])
def list_partner_performances():
    """List all partner performances"""
    return partner_performances_db

@router.get("/performance/{performance_id}", response_model=PartnerPerformance)
def get_partner_performance(performance_id: int):
    """Get a specific partner performance by ID"""
    for performance in partner_performances_db:
        if performance.id == performance_id:
            return performance
    raise HTTPException(status_code=404, detail="Partner performance not found")

@router.post("/performance", response_model=PartnerPerformance)
def create_partner_performance(performance: PartnerPerformanceCreate):
    """Create a new partner performance record"""
    new_id = max([p.id for p in partner_performances_db]) + 1 if partner_performances_db else 1
    new_performance = PartnerPerformance(
        id=new_id,
        created_at=datetime.now(),
        **performance.dict()
    )
    partner_performances_db.append(new_performance)
    return new_performance

@router.put("/performance/{performance_id}", response_model=PartnerPerformance)
def update_partner_performance(performance_id: int, performance_update: PartnerPerformanceUpdate):
    """Update an existing partner performance record"""
    for index, performance in enumerate(partner_performances_db):
        if performance.id == performance_id:
            updated_performance = PartnerPerformance(
                id=performance_id,
                created_at=performance.created_at,
                **performance_update.dict()
            )
            partner_performances_db[index] = updated_performance
            return updated_performance
    raise HTTPException(status_code=404, detail="Partner performance not found")

@router.delete("/performance/{performance_id}")
def delete_partner_performance(performance_id: int):
    """Delete a partner performance record"""
    for index, performance in enumerate(partner_performances_db):
        if performance.id == performance_id:
            del partner_performances_db[index]
            return {"message": "Partner performance deleted successfully"}
    raise HTTPException(status_code=404, detail="Partner performance not found")

@router.get("/performance/partner/{partner_id}", response_model=List[PartnerPerformance])
def get_partner_performance_history(partner_id: int):
    """Get performance history for a partner"""
    return [performance for performance in partner_performances_db if performance.partner_id == partner_id]

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_partner_status_options():
    """Get available partner statuses"""
    return get_partner_statuses()

@router.get("/config/types", response_model=List[str])
def get_partner_type_options():
    """Get available partner types"""
    return get_partner_types()