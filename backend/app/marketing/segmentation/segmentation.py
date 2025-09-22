from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from .models import (
    Audience, AudienceCreate, AudienceUpdate,
    SegmentCriteria, SegmentCriteriaCreate, SegmentCriteriaUpdate,
    CustomAudience, CustomAudienceCreate, CustomAudienceUpdate,
    DemographicTargeting, DemographicTargetingCreate, DemographicTargetingUpdate,
    BehavioralTargeting, BehavioralTargetingCreate, BehavioralTargetingUpdate,
    AccountBasedMarketing, AccountBasedMarketingCreate, AccountBasedMarketingUpdate
)
from .config import (
    get_segment_types, get_segment_criteria_types,
    get_default_member_count, get_default_target_count
)

router = APIRouter()

# In-memory storage for demo purposes
audiences_db = []
segment_criteria_db = []
custom_audiences_db = []
demographic_targetings_db = []
behavioral_targetings_db = []
account_based_marketings_db = []

@router.get("/audiences", response_model=List[Audience])
def list_audiences():
    """List all audiences"""
    return audiences_db

@router.get("/audiences/{audience_id}", response_model=Audience)
def get_audience(audience_id: int):
    """Get a specific audience by ID"""
    for audience in audiences_db:
        if audience.id == audience_id:
            return audience
    raise HTTPException(status_code=404, detail="Audience not found")

@router.post("/audiences", response_model=Audience)
def create_audience(audience: AudienceCreate):
    """Create a new audience"""
    new_id = max([a.id for a in audiences_db]) + 1 if audiences_db else 1
    new_audience = Audience(
        id=new_id,
        created_at=datetime.now(),
        member_count=get_default_member_count(),
        **audience.dict()
    )
    audiences_db.append(new_audience)
    return new_audience

@router.put("/audiences/{audience_id}", response_model=Audience)
def update_audience(audience_id: int, audience_update: AudienceUpdate):
    """Update an existing audience"""
    for index, audience in enumerate(audiences_db):
        if audience.id == audience_id:
            updated_audience = Audience(
                id=audience_id,
                created_at=audience.created_at,
                updated_at=datetime.now(),
                member_count=audience.member_count,
                **audience_update.dict()
            )
            audiences_db[index] = updated_audience
            return updated_audience
    raise HTTPException(status_code=404, detail="Audience not found")

@router.delete("/audiences/{audience_id}")
def delete_audience(audience_id: int):
    """Delete an audience"""
    for index, audience in enumerate(audiences_db):
        if audience.id == audience_id:
            del audiences_db[index]
            return {"message": "Audience deleted successfully"}
    raise HTTPException(status_code=404, detail="Audience not found")

@router.get("/audiences/type/{segment_type}", response_model=List[Audience])
def get_audiences_by_type(segment_type: str):
    """Get audiences by segment type"""
    # Normalize the segment_type parameter to handle case differences
    normalized_type = segment_type.lower().title()
    return [audience for audience in audiences_db if audience.segment_type.value == normalized_type]

@router.post("/audiences/{audience_id}/refresh")
def refresh_audience(audience_id: int):
    """Refresh an audience membership"""
    for index, audience in enumerate(audiences_db):
        if audience.id == audience_id:
            # In a real implementation, you would recalculate the audience membership
            audience.member_count = get_default_member_count() + 100  # Simulated refresh
            audience.updated_at = datetime.now()
            audiences_db[index] = audience
            return {"message": f"Audience {audience_id} refreshed successfully"}
    raise HTTPException(status_code=404, detail="Audience not found")

# Segment Criteria endpoints
@router.get("/criteria", response_model=List[SegmentCriteria])
def list_segment_criteria():
    """List all segment criteria"""
    return segment_criteria_db

@router.get("/criteria/{criteria_id}", response_model=SegmentCriteria)
def get_segment_criteria(criteria_id: int):
    """Get a specific segment criteria by ID"""
    for criteria in segment_criteria_db:
        if criteria.id == criteria_id:
            return criteria
    raise HTTPException(status_code=404, detail="Segment criteria not found")

@router.post("/criteria", response_model=SegmentCriteria)
def create_segment_criteria(criteria: SegmentCriteriaCreate):
    """Create a new segment criteria"""
    new_id = max([c.id for c in segment_criteria_db]) + 1 if segment_criteria_db else 1
    new_criteria = SegmentCriteria(
        id=new_id,
        created_at=datetime.now(),
        **criteria.dict()
    )
    segment_criteria_db.append(new_criteria)
    return new_criteria

@router.put("/criteria/{criteria_id}", response_model=SegmentCriteria)
def update_segment_criteria(criteria_id: int, criteria_update: SegmentCriteriaUpdate):
    """Update an existing segment criteria"""
    for index, criteria in enumerate(segment_criteria_db):
        if criteria.id == criteria_id:
            updated_criteria = SegmentCriteria(
                id=criteria_id,
                created_at=criteria.created_at,
                updated_at=datetime.now(),
                **criteria_update.dict()
            )
            segment_criteria_db[index] = updated_criteria
            return updated_criteria
    raise HTTPException(status_code=404, detail="Segment criteria not found")

@router.delete("/criteria/{criteria_id}")
def delete_segment_criteria(criteria_id: int):
    """Delete a segment criteria"""
    for index, criteria in enumerate(segment_criteria_db):
        if criteria.id == criteria_id:
            del segment_criteria_db[index]
            return {"message": "Segment criteria deleted successfully"}
    raise HTTPException(status_code=404, detail="Segment criteria not found")

@router.get("/criteria/audience/{audience_id}", response_model=List[SegmentCriteria])
def get_segment_criteria_by_audience(audience_id: int):
    """Get segment criteria by audience ID"""
    return [criteria for criteria in segment_criteria_db if criteria.audience_id == audience_id]

# Custom Audiences endpoints
@router.get("/custom-audiences", response_model=List[CustomAudience])
def list_custom_audiences():
    """List all custom audiences"""
    return custom_audiences_db

@router.get("/custom-audiences/{audience_id}", response_model=CustomAudience)
def get_custom_audience(audience_id: int):
    """Get a specific custom audience by ID"""
    for audience in custom_audiences_db:
        if audience.id == audience_id:
            return audience
    raise HTTPException(status_code=404, detail="Custom audience not found")

@router.post("/custom-audiences", response_model=CustomAudience)
def create_custom_audience(audience: CustomAudienceCreate):
    """Create a new custom audience"""
    new_id = max([a.id for a in custom_audiences_db]) + 1 if custom_audiences_db else 1
    new_audience = CustomAudience(
        id=new_id,
        created_at=datetime.now(),
        member_count=len(audience.member_ids),
        **audience.dict()
    )
    custom_audiences_db.append(new_audience)
    return new_audience

@router.put("/custom-audiences/{audience_id}", response_model=CustomAudience)
def update_custom_audience(audience_id: int, audience_update: CustomAudienceUpdate):
    """Update an existing custom audience"""
    for index, audience in enumerate(custom_audiences_db):
        if audience.id == audience_id:
            updated_audience = CustomAudience(
                id=audience_id,
                created_at=audience.created_at,
                updated_at=datetime.now(),
                member_count=len(audience_update.member_ids) if audience_update.member_ids else audience.member_count,
                **audience_update.dict()
            )
            custom_audiences_db[index] = updated_audience
            return updated_audience
    raise HTTPException(status_code=404, detail="Custom audience not found")

@router.delete("/custom-audiences/{audience_id}")
def delete_custom_audience(audience_id: int):
    """Delete a custom audience"""
    for index, audience in enumerate(custom_audiences_db):
        if audience.id == audience_id:
            del custom_audiences_db[index]
            return {"message": "Custom audience deleted successfully"}
    raise HTTPException(status_code=404, detail="Custom audience not found")

# Demographic Targeting endpoints
@router.get("/demographic-targeting", response_model=List[DemographicTargeting])
def list_demographic_targetings():
    """List all demographic targetings"""
    return demographic_targetings_db

@router.get("/demographic-targeting/{targeting_id}", response_model=DemographicTargeting)
def get_demographic_targeting(targeting_id: int):
    """Get a specific demographic targeting by ID"""
    for targeting in demographic_targetings_db:
        if targeting.id == targeting_id:
            return targeting
    raise HTTPException(status_code=404, detail="Demographic targeting not found")

@router.post("/demographic-targeting", response_model=DemographicTargeting)
def create_demographic_targeting(targeting: DemographicTargetingCreate):
    """Create a new demographic targeting"""
    new_id = max([t.id for t in demographic_targetings_db]) + 1 if demographic_targetings_db else 1
    new_targeting = DemographicTargeting(
        id=new_id,
        created_at=datetime.now(),
        target_count=get_default_target_count(),
        **targeting.dict()
    )
    demographic_targetings_db.append(new_targeting)
    return new_targeting

@router.put("/demographic-targeting/{targeting_id}", response_model=DemographicTargeting)
def update_demographic_targeting(targeting_id: int, targeting_update: DemographicTargetingUpdate):
    """Update an existing demographic targeting"""
    for index, targeting in enumerate(demographic_targetings_db):
        if targeting.id == targeting_id:
            updated_targeting = DemographicTargeting(
                id=targeting_id,
                created_at=targeting.created_at,
                updated_at=datetime.now(),
                target_count=targeting.target_count,
                **targeting_update.dict()
            )
            demographic_targetings_db[index] = updated_targeting
            return updated_targeting
    raise HTTPException(status_code=404, detail="Demographic targeting not found")

@router.delete("/demographic-targeting/{targeting_id}")
def delete_demographic_targeting(targeting_id: int):
    """Delete a demographic targeting"""
    for index, targeting in enumerate(demographic_targetings_db):
        if targeting.id == targeting_id:
            del demographic_targetings_db[index]
            return {"message": "Demographic targeting deleted successfully"}
    raise HTTPException(status_code=404, detail="Demographic targeting not found")

# Behavioral Targeting endpoints
@router.get("/behavioral-targeting", response_model=List[BehavioralTargeting])
def list_behavioral_targetings():
    """List all behavioral targetings"""
    return behavioral_targetings_db

@router.get("/behavioral-targeting/{targeting_id}", response_model=BehavioralTargeting)
def get_behavioral_targeting(targeting_id: int):
    """Get a specific behavioral targeting by ID"""
    for targeting in behavioral_targetings_db:
        if targeting.id == targeting_id:
            return targeting
    raise HTTPException(status_code=404, detail="Behavioral targeting not found")

@router.post("/behavioral-targeting", response_model=BehavioralTargeting)
def create_behavioral_targeting(targeting: BehavioralTargetingCreate):
    """Create a new behavioral targeting"""
    new_id = max([t.id for t in behavioral_targetings_db]) + 1 if behavioral_targetings_db else 1
    new_targeting = BehavioralTargeting(
        id=new_id,
        created_at=datetime.now(),
        target_count=get_default_target_count(),
        **targeting.dict()
    )
    behavioral_targetings_db.append(new_targeting)
    return new_targeting

@router.put("/behavioral-targeting/{targeting_id}", response_model=BehavioralTargeting)
def update_behavioral_targeting(targeting_id: int, targeting_update: BehavioralTargetingUpdate):
    """Update an existing behavioral targeting"""
    for index, targeting in enumerate(behavioral_targetings_db):
        if targeting.id == targeting_id:
            updated_targeting = BehavioralTargeting(
                id=targeting_id,
                created_at=targeting.created_at,
                updated_at=datetime.now(),
                target_count=targeting.target_count,
                **targeting_update.dict()
            )
            behavioral_targetings_db[index] = updated_targeting
            return updated_targeting
    raise HTTPException(status_code=404, detail="Behavioral targeting not found")

@router.delete("/behavioral-targeting/{targeting_id}")
def delete_behavioral_targeting(targeting_id: int):
    """Delete a behavioral targeting"""
    for index, targeting in enumerate(behavioral_targetings_db):
        if targeting.id == targeting_id:
            del behavioral_targetings_db[index]
            return {"message": "Behavioral targeting deleted successfully"}
    raise HTTPException(status_code=404, detail="Behavioral targeting not found")

# Account-Based Marketing endpoints
@router.get("/abm", response_model=List[AccountBasedMarketing])
def list_account_based_marketings():
    """List all account-based marketings"""
    return account_based_marketings_db

@router.get("/abm/{abm_id}", response_model=AccountBasedMarketing)
def get_account_based_marketing(abm_id: int):
    """Get a specific account-based marketing by ID"""
    for abm in account_based_marketings_db:
        if abm.id == abm_id:
            return abm
    raise HTTPException(status_code=404, detail="Account-based marketing not found")

@router.post("/abm", response_model=AccountBasedMarketing)
def create_account_based_marketing(abm: AccountBasedMarketingCreate):
    """Create a new account-based marketing"""
    new_id = max([a.id for a in account_based_marketings_db]) + 1 if account_based_marketings_db else 1
    new_abm = AccountBasedMarketing(
        id=new_id,
        created_at=datetime.now(),
        account_count=len(abm.company_ids),
        **abm.dict()
    )
    account_based_marketings_db.append(new_abm)
    return new_abm

@router.put("/abm/{abm_id}", response_model=AccountBasedMarketing)
def update_account_based_marketing(abm_id: int, abm_update: AccountBasedMarketingUpdate):
    """Update an existing account-based marketing"""
    for index, abm in enumerate(account_based_marketings_db):
        if abm.id == abm_id:
            updated_abm = AccountBasedMarketing(
                id=abm_id,
                created_at=abm.created_at,
                updated_at=datetime.now(),
                account_count=len(abm_update.company_ids) if abm_update.company_ids else abm.account_count,
                **abm_update.dict()
            )
            account_based_marketings_db[index] = updated_abm
            return updated_abm
    raise HTTPException(status_code=404, detail="Account-based marketing not found")

@router.delete("/abm/{abm_id}")
def delete_account_based_marketing(abm_id: int):
    """Delete an account-based marketing"""
    for index, abm in enumerate(account_based_marketings_db):
        if abm.id == abm_id:
            del account_based_marketings_db[index]
            return {"message": "Account-based marketing deleted successfully"}
    raise HTTPException(status_code=404, detail="Account-based marketing not found")

# Configuration endpoints
@router.get("/config/segment-types", response_model=List[str])
def get_segment_type_options():
    """Get available segment types"""
    return get_segment_types()

@router.get("/config/criteria-types", response_model=List[str])
def get_segment_criteria_type_options():
    """Get available segment criteria types"""
    return get_segment_criteria_types()