from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    CustomerDataProfile, CustomerDataProfileCreate, CustomerDataProfileUpdate,
    DataIntegration, DataIntegrationCreate, DataIntegrationUpdate,
    IdentityResolution, IdentityResolutionCreate, IdentityResolutionUpdate,
    RealTimeSegment, RealTimeSegmentCreate, RealTimeSegmentUpdate,
    DataPrivacy, DataPrivacyCreate, DataPrivacyUpdate,
    DataQuality, DataQualityCreate, DataQualityUpdate
)
from .config import (
    get_data_source_types, get_identity_resolution_statuses, get_data_privacy_statuses,
    get_default_profile_score, get_default_engagement_score,
    get_default_completeness_score, get_default_accuracy_score
)

router = APIRouter()

# In-memory storage for demo purposes
customer_profiles_db = []
data_integrations_db = []
identity_resolutions_db = []
real_time_segments_db = []
data_privacy_records_db = []
data_quality_records_db = []

@router.get("/")
def get_cdp_dashboard():
    """Get Customer Data Platform dashboard with summary statistics"""
    return {
        "message": "Customer Data Platform Dashboard",
        "statistics": {
            "total_profiles": len(customer_profiles_db),
            "data_integrations": len(data_integrations_db),
            "identity_resolutions": len(identity_resolutions_db),
            "real_time_segments": len(real_time_segments_db)
        }
    }

@router.get("/profiles", response_model=List[CustomerDataProfile])
def list_customer_profiles():
    """List all customer data profiles"""
    return customer_profiles_db

@router.get("/profiles/{profile_id}", response_model=CustomerDataProfile)
def get_customer_profile(profile_id: int):
    """Get a specific customer data profile by ID"""
    for profile in customer_profiles_db:
        if profile.id == profile_id:
            return profile
    raise HTTPException(status_code=404, detail="Customer profile not found")

@router.post("/profiles", response_model=CustomerDataProfile)
def create_customer_profile(profile: CustomerDataProfileCreate):
    """Create a new customer data profile"""
    new_id = max([p.id for p in customer_profiles_db]) + 1 if customer_profiles_db else 1
    new_profile = CustomerDataProfile(
        id=new_id,
        created_at=datetime.now(),
        profile_score=get_default_profile_score(),
        engagement_score=get_default_engagement_score(),
        lifetime_value=0.0,
        **profile.dict()
    )
    customer_profiles_db.append(new_profile)
    return new_profile

@router.put("/profiles/{profile_id}", response_model=CustomerDataProfile)
def update_customer_profile(profile_id: int, profile_update: CustomerDataProfileUpdate):
    """Update an existing customer data profile"""
    for index, profile in enumerate(customer_profiles_db):
        if profile.id == profile_id:
            updated_profile = CustomerDataProfile(
                id=profile_id,
                created_at=profile.created_at,
                updated_at=datetime.now(),
                profile_score=profile.profile_score,
                engagement_score=profile.engagement_score,
                lifetime_value=profile.lifetime_value,
                **profile_update.dict()
            )
            customer_profiles_db[index] = updated_profile
            return updated_profile
    raise HTTPException(status_code=404, detail="Customer profile not found")

@router.delete("/profiles/{profile_id}")
def delete_customer_profile(profile_id: int):
    """Delete a customer data profile"""
    for index, profile in enumerate(customer_profiles_db):
        if profile.id == profile_id:
            del customer_profiles_db[index]
            return {"message": "Customer profile deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer profile not found")

@router.get("/profiles/search", response_model=List[CustomerDataProfile])
def search_customer_profiles(query: str):
    """Search customer profiles by name, email, or phone"""
    results = []
    for profile in customer_profiles_db:
        if (query.lower() in profile.full_name.lower() or 
            (profile.email and query.lower() in profile.email.lower()) or 
            (profile.phone and query in profile.phone)):
            results.append(profile)
    return results

@router.post("/profiles/{profile_id}/calculate-ltv")
def calculate_customer_lifetime_value(profile_id: int, transactions: List[Dict[str, Any]]):
    """Calculate customer lifetime value based on transaction data"""
    for index, profile in enumerate(customer_profiles_db):
        if profile.id == profile_id:
            # Simplified LTV calculation
            total_value = sum(transaction.get("amount", 0) for transaction in transactions)
            profile.lifetime_value = total_value
            profile.updated_at = datetime.now()
            customer_profiles_db[index] = profile
            return {"message": f"LTV calculated for profile {profile_id}", "lifetime_value": total_value}
    raise HTTPException(status_code=404, detail="Customer profile not found")

# Data Integrations endpoints
@router.get("/integrations", response_model=List[DataIntegration])
def list_data_integrations():
    """List all data integrations"""
    return data_integrations_db

@router.get("/integrations/{integration_id}", response_model=DataIntegration)
def get_data_integration(integration_id: int):
    """Get a specific data integration by ID"""
    for integration in data_integrations_db:
        if integration.id == integration_id:
            return integration
    raise HTTPException(status_code=404, detail="Data integration not found")

@router.post("/integrations", response_model=DataIntegration)
def create_data_integration(integration: DataIntegrationCreate):
    """Create a new data integration"""
    new_id = max([i.id for i in data_integrations_db]) + 1 if data_integrations_db else 1
    new_integration = DataIntegration(
        id=new_id,
        created_at=datetime.now(),
        records_processed=0,
        last_sync_status="Success",
        **integration.dict()
    )
    data_integrations_db.append(new_integration)
    return new_integration

@router.put("/integrations/{integration_id}", response_model=DataIntegration)
def update_data_integration(integration_id: int, integration_update: DataIntegrationUpdate):
    """Update an existing data integration"""
    for index, integration in enumerate(data_integrations_db):
        if integration.id == integration_id:
            updated_integration = DataIntegration(
                id=integration_id,
                created_at=integration.created_at,
                updated_at=datetime.now(),
                records_processed=integration.records_processed,
                last_sync_status=integration.last_sync_status,
                last_sync=integration.last_sync,
                **integration_update.dict()
            )
            data_integrations_db[index] = updated_integration
            return updated_integration
    raise HTTPException(status_code=404, detail="Data integration not found")

@router.delete("/integrations/{integration_id}")
def delete_data_integration(integration_id: int):
    """Delete a data integration"""
    for index, integration in enumerate(data_integrations_db):
        if integration.id == integration_id:
            del data_integrations_db[index]
            return {"message": "Data integration deleted successfully"}
    raise HTTPException(status_code=404, detail="Data integration not found")

@router.post("/integrations/{integration_id}/sync")
def sync_data_integration(integration_id: int):
    """Trigger a sync for a data integration"""
    for index, integration in enumerate(data_integrations_db):
        if integration.id == integration_id:
            integration.last_sync = datetime.now()
            integration.records_processed += 100  # Simulated record count
            integration.last_sync_status = "Success"
            integration.updated_at = datetime.now()
            data_integrations_db[index] = integration
            return {"message": f"Data integration {integration_id} synced successfully"}
    raise HTTPException(status_code=404, detail="Data integration not found")

# Identity Resolutions endpoints
@router.get("/identity-resolutions", response_model=List[IdentityResolution])
def list_identity_resolutions():
    """List all identity resolutions"""
    return identity_resolutions_db

@router.get("/identity-resolutions/{resolution_id}", response_model=IdentityResolution)
def get_identity_resolution(resolution_id: int):
    """Get a specific identity resolution by ID"""
    for resolution in identity_resolutions_db:
        if resolution.id == resolution_id:
            return resolution
    raise HTTPException(status_code=404, detail="Identity resolution not found")

@router.post("/identity-resolutions", response_model=IdentityResolution)
def create_identity_resolution(resolution: IdentityResolutionCreate):
    """Create a new identity resolution"""
    new_id = max([r.id for r in identity_resolutions_db]) + 1 if identity_resolutions_db else 1
    new_resolution = IdentityResolution(
        id=new_id,
        created_at=datetime.now(),
        **resolution.dict()
    )
    identity_resolutions_db.append(new_resolution)
    return new_resolution

@router.put("/identity-resolutions/{resolution_id}", response_model=IdentityResolution)
def update_identity_resolution(resolution_id: int, resolution_update: IdentityResolutionUpdate):
    """Update an existing identity resolution"""
    for index, resolution in enumerate(identity_resolutions_db):
        if resolution.id == resolution_id:
            updated_resolution = IdentityResolution(
                id=resolution_id,
                created_at=resolution.created_at,
                updated_at=datetime.now(),
                **resolution_update.dict()
            )
            identity_resolutions_db[index] = updated_resolution
            return updated_resolution
    raise HTTPException(status_code=404, detail="Identity resolution not found")

@router.delete("/identity-resolutions/{resolution_id}")
def delete_identity_resolution(resolution_id: int):
    """Delete an identity resolution"""
    for index, resolution in enumerate(identity_resolutions_db):
        if resolution.id == resolution_id:
            del identity_resolutions_db[index]
            return {"message": "Identity resolution deleted successfully"}
    raise HTTPException(status_code=404, detail="Identity resolution not found")

@router.post("/identity-resolutions/{resolution_id}/merge")
def merge_customer_profiles(resolution_id: int):
    """Merge duplicate customer profiles"""
    for index, resolution in enumerate(identity_resolutions_db):
        if resolution.id == resolution_id:
            resolution.resolution_status = "Merged"
            resolution.resolved_by = "System"
            resolution.updated_at = datetime.now()
            identity_resolutions_db[index] = resolution
            
            # In a real implementation, you would actually merge the profile data
            return {"message": f"Customer profiles merged for resolution {resolution_id}"}
    raise HTTPException(status_code=404, detail="Identity resolution not found")

# Real-Time Segments endpoints
@router.get("/segments", response_model=List[RealTimeSegment])
def list_real_time_segments():
    """List all real-time segments"""
    return real_time_segments_db

@router.get("/segments/{segment_id}", response_model=RealTimeSegment)
def get_real_time_segment(segment_id: int):
    """Get a specific real-time segment by ID"""
    for segment in real_time_segments_db:
        if segment.id == segment_id:
            return segment
    raise HTTPException(status_code=404, detail="Real-time segment not found")

@router.post("/segments", response_model=RealTimeSegment)
def create_real_time_segment(segment: RealTimeSegmentCreate):
    """Create a new real-time segment"""
    new_id = max([s.id for s in real_time_segments_db]) + 1 if real_time_segments_db else 1
    new_segment = RealTimeSegment(
        id=new_id,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        **segment.dict()
    )
    real_time_segments_db.append(new_segment)
    return new_segment

@router.put("/segments/{segment_id}", response_model=RealTimeSegment)
def update_real_time_segment(segment_id: int, segment_update: RealTimeSegmentUpdate):
    """Update an existing real-time segment"""
    for index, segment in enumerate(real_time_segments_db):
        if segment.id == segment_id:
            updated_segment = RealTimeSegment(
                id=segment_id,
                created_at=segment.created_at,
                updated_at=datetime.now(),
                last_updated=datetime.now(),
                member_count=segment.member_count,
                **segment_update.dict()
            )
            real_time_segments_db[index] = updated_segment
            return updated_segment
    raise HTTPException(status_code=404, detail="Real-time segment not found")

@router.delete("/segments/{segment_id}")
def delete_real_time_segment(segment_id: int):
    """Delete a real-time segment"""
    for index, segment in enumerate(real_time_segments_db):
        if segment.id == segment_id:
            del real_time_segments_db[index]
            return {"message": "Real-time segment deleted successfully"}
    raise HTTPException(status_code=404, detail="Real-time segment not found")

@router.post("/segments/{segment_id}/refresh")
def refresh_real_time_segment(segment_id: int):
    """Refresh a real-time segment membership"""
    for index, segment in enumerate(real_time_segments_db):
        if segment.id == segment_id:
            segment.member_count = segment.member_count + 10  # Simulated refresh
            segment.last_updated = datetime.now()
            segment.updated_at = datetime.now()
            real_time_segments_db[index] = segment
            return {"message": f"Real-time segment {segment_id} refreshed"}
    raise HTTPException(status_code=404, detail="Real-time segment not found")

# Data Privacy endpoints
@router.get("/privacy", response_model=List[DataPrivacy])
def list_data_privacy_records():
    """List all data privacy records"""
    return data_privacy_records_db

@router.get("/privacy/{privacy_id}", response_model=DataPrivacy)
def get_data_privacy_record(privacy_id: int):
    """Get a specific data privacy record by ID"""
    for record in data_privacy_records_db:
        if record.id == privacy_id:
            return record
    raise HTTPException(status_code=404, detail="Data privacy record not found")

@router.post("/privacy", response_model=DataPrivacy)
def create_data_privacy_record(record: DataPrivacyCreate):
    """Create a new data privacy record"""
    new_id = max([r.id for r in data_privacy_records_db]) + 1 if data_privacy_records_db else 1
    new_record = DataPrivacy(
        id=new_id,
        created_at=datetime.now(),
        **record.dict()
    )
    data_privacy_records_db.append(new_record)
    return new_record

@router.put("/privacy/{privacy_id}", response_model=DataPrivacy)
def update_data_privacy_record(privacy_id: int, record_update: DataPrivacyUpdate):
    """Update an existing data privacy record"""
    for index, record in enumerate(data_privacy_records_db):
        if record.id == privacy_id:
            updated_record = DataPrivacy(
                id=privacy_id,
                created_at=record.created_at,
                updated_at=datetime.now(),
                **record_update.dict()
            )
            data_privacy_records_db[index] = updated_record
            return updated_record
    raise HTTPException(status_code=404, detail="Data privacy record not found")

@router.delete("/privacy/{privacy_id}")
def delete_data_privacy_record(privacy_id: int):
    """Delete a data privacy record"""
    for index, record in enumerate(data_privacy_records_db):
        if record.id == privacy_id:
            del data_privacy_records_db[index]
            return {"message": "Data privacy record deleted successfully"}
    raise HTTPException(status_code=404, detail="Data privacy record not found")

@router.post("/privacy/{privacy_id}/restrict")
def restrict_data_processing(privacy_id: int):
    """Restrict data processing for a customer"""
    for index, record in enumerate(data_privacy_records_db):
        if record.id == privacy_id:
            record.privacy_status = "Restricted"
            record.updated_at = datetime.now()
            data_privacy_records_db[index] = record
            return {"message": f"Data processing restricted for privacy record {privacy_id}"}
    raise HTTPException(status_code=404, detail="Data privacy record not found")

# Data Quality endpoints
@router.get("/quality", response_model=List[DataQuality])
def list_data_quality_records():
    """List all data quality records"""
    return data_quality_records_db

@router.get("/quality/{quality_id}", response_model=DataQuality)
def get_data_quality_record(quality_id: int):
    """Get a specific data quality record by ID"""
    for record in data_quality_records_db:
        if record.id == quality_id:
            return record
    raise HTTPException(status_code=404, detail="Data quality record not found")

@router.post("/quality", response_model=DataQuality)
def create_data_quality_record(record: DataQualityCreate):
    """Create a new data quality record"""
    new_id = max([r.id for r in data_quality_records_db]) + 1 if data_quality_records_db else 1
    new_record = DataQuality(
        id=new_id,
        created_at=datetime.now(),
        **record.dict()
    )
    data_quality_records_db.append(new_record)
    return new_record

@router.put("/quality/{quality_id}", response_model=DataQuality)
def update_data_quality_record(quality_id: int, record_update: DataQualityUpdate):
    """Update an existing data quality record"""
    for index, record in enumerate(data_quality_records_db):
        if record.id == quality_id:
            # Recalculate overall score
            scores = [
                record_update.completeness_score,
                record_update.accuracy_score,
                record_update.consistency_score,
                record_update.freshness_score
            ]
            overall_score = sum(scores) / len(scores) if scores else 0.0
            
            updated_record = DataQuality(
                id=quality_id,
                created_at=record.created_at,
                updated_at=datetime.now(),
                overall_score=overall_score,
                **record_update.dict()
            )
            data_quality_records_db[index] = updated_record
            return updated_record
    raise HTTPException(status_code=404, detail="Data quality record not found")

@router.delete("/quality/{quality_id}")
def delete_data_quality_record(quality_id: int):
    """Delete a data quality record"""
    for index, record in enumerate(data_quality_records_db):
        if record.id == quality_id:
            del data_quality_records_db[index]
            return {"message": "Data quality record deleted successfully"}
    raise HTTPException(status_code=404, detail="Data quality record not found")

@router.post("/quality/{quality_id}/validate")
def validate_data_quality(quality_id: int):
    """Validate and update data quality scores"""
    for index, record in enumerate(data_quality_records_db):
        if record.id == quality_id:
            # Simulated validation - in a real implementation, you would run actual data quality checks
            record.completeness_score = min(1.0, record.completeness_score + 0.1)
            record.accuracy_score = min(1.0, record.accuracy_score + 0.05)
            record.consistency_score = min(1.0, record.consistency_score + 0.05)
            record.freshness_score = min(1.0, record.freshness_score + 0.1)
            
            # Recalculate overall score
            scores = [
                record.completeness_score,
                record.accuracy_score,
                record.consistency_score,
                record.freshness_score
            ]
            record.overall_score = sum(scores) / len(scores)
            
            record.last_validated = datetime.now()
            record.updated_at = datetime.now()
            data_quality_records_db[index] = record
            return {"message": f"Data quality validated for record {quality_id}"}
    raise HTTPException(status_code=404, detail="Data quality record not found")

# Configuration endpoints
@router.get("/config/source-types", response_model=List[str])
def get_data_source_type_options():
    """Get available data source types"""
    return get_data_source_types()

@router.get("/config/resolution-statuses", response_model=List[str])
def get_identity_resolution_status_options():
    """Get available identity resolution statuses"""
    return get_identity_resolution_statuses()

@router.get("/config/privacy-statuses", response_model=List[str])
def get_data_privacy_status_options():
    """Get available data privacy statuses"""
    return get_data_privacy_statuses()