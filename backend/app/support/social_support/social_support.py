from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    SocialInquiry, SocialInquiryCreate, SocialInquiryUpdate,
    SocialResponse, SocialResponseCreate,
    SocialTemplate, SocialTemplateCreate, SocialTemplateUpdate
)
from .config import (
    get_social_platforms, get_social_sentiments, 
    get_default_sentiment, get_max_tags_per_inquiry
)

router = APIRouter()

# In-memory storage for demo purposes
social_inquiries_db = []
social_responses_db = []
social_templates_db = []

@router.get("/inquiries", response_model=List[SocialInquiry])
def list_social_inquiries():
    """List all social inquiries"""
    return social_inquiries_db

@router.get("/inquiries/{inquiry_id}", response_model=SocialInquiry)
def get_social_inquiry(inquiry_id: int):
    """Get a specific social inquiry by ID"""
    for inquiry in social_inquiries_db:
        if inquiry.id == inquiry_id:
            return inquiry
    raise HTTPException(status_code=404, detail="Social inquiry not found")

@router.post("/inquiries", response_model=SocialInquiry)
def create_social_inquiry(inquiry: SocialInquiryCreate):
    """Create a new social inquiry"""
    new_id = max([i.id for i in social_inquiries_db]) + 1 if social_inquiries_db else 1
    new_inquiry = SocialInquiry(
        id=new_id,
        created_at=datetime.now(),
        **inquiry.dict()
    )
    social_inquiries_db.append(new_inquiry)
    return new_inquiry

@router.put("/inquiries/{inquiry_id}", response_model=SocialInquiry)
def update_social_inquiry(inquiry_id: int, inquiry_update: SocialInquiryUpdate):
    """Update an existing social inquiry"""
    for index, inquiry in enumerate(social_inquiries_db):
        if inquiry.id == inquiry_id:
            updated_inquiry = SocialInquiry(
                id=inquiry_id,
                created_at=inquiry.created_at,
                updated_at=datetime.now(),
                **inquiry_update.dict()
            )
            social_inquiries_db[index] = updated_inquiry
            return updated_inquiry
    raise HTTPException(status_code=404, detail="Social inquiry not found")

@router.delete("/inquiries/{inquiry_id}")
def delete_social_inquiry(inquiry_id: int):
    """Delete a social inquiry"""
    for index, inquiry in enumerate(social_inquiries_db):
        if inquiry.id == inquiry_id:
            del social_inquiries_db[index]
            return {"message": "Social inquiry deleted successfully"}
    raise HTTPException(status_code=404, detail="Social inquiry not found")

@router.post("/inquiries/{inquiry_id}/assign")
def assign_social_inquiry(inquiry_id: int, agent_id: str):
    """Assign a social inquiry to an agent"""
    for index, inquiry in enumerate(social_inquiries_db):
        if inquiry.id == inquiry_id:
            social_inquiries_db[index].assigned_agent_id = agent_id
            return {"message": "Social inquiry assigned successfully"}
    raise HTTPException(status_code=404, detail="Social inquiry not found")

@router.post("/inquiries/{inquiry_id}/respond")
def respond_to_social_inquiry(inquiry_id: int):
    """Mark a social inquiry as responded"""
    for index, inquiry in enumerate(social_inquiries_db):
        if inquiry.id == inquiry_id:
            social_inquiries_db[index].responded_at = datetime.now()
            return {"message": "Social inquiry marked as responded"}
    raise HTTPException(status_code=404, detail="Social inquiry not found")

@router.get("/inquiries/customer/{customer_id}", response_model=List[SocialInquiry])
def get_social_inquiries_by_customer(customer_id: int):
    """Get social inquiries by customer ID"""
    return [inquiry for inquiry in social_inquiries_db if inquiry.customer_id == customer_id]

@router.get("/inquiries/agent/{agent_id}", response_model=List[SocialInquiry])
def get_social_inquiries_by_agent(agent_id: str):
    """Get social inquiries by agent ID"""
    return [inquiry for inquiry in social_inquiries_db if inquiry.assigned_agent_id == agent_id]

@router.get("/inquiries/platform/{platform}", response_model=List[SocialInquiry])
def get_social_inquiries_by_platform(platform: str):
    """Get social inquiries by platform"""
    # Normalize the platform parameter to handle case differences
    normalized_platform = platform.lower().title()
    return [inquiry for inquiry in social_inquiries_db if inquiry.platform.value == normalized_platform]

@router.get("/inquiries/sentiment/{sentiment}", response_model=List[SocialInquiry])
def get_social_inquiries_by_sentiment(sentiment: str):
    """Get social inquiries by sentiment"""
    # Normalize the sentiment parameter to handle case differences
    normalized_sentiment = sentiment.lower().title()
    return [inquiry for inquiry in social_inquiries_db if inquiry.sentiment.value == normalized_sentiment]

# Social Response endpoints
@router.get("/responses", response_model=List[SocialResponse])
def list_social_responses():
    """List all social responses"""
    return social_responses_db

@router.get("/responses/{response_id}", response_model=SocialResponse)
def get_social_response(response_id: int):
    """Get a specific social response by ID"""
    for response in social_responses_db:
        if response.id == response_id:
            return response
    raise HTTPException(status_code=404, detail="Social response not found")

@router.post("/responses", response_model=SocialResponse)
def create_social_response(response: SocialResponseCreate):
    """Create a new social response"""
    new_id = max([r.id for r in social_responses_db]) + 1 if social_responses_db else 1
    new_response = SocialResponse(
        id=new_id,
        created_at=datetime.now(),
        **response.dict()
    )
    social_responses_db.append(new_response)
    return new_response

@router.put("/responses/{response_id}", response_model=SocialResponse)
def update_social_response(response_id: int, response_update: SocialResponseCreate):
    """Update an existing social response"""
    for index, response in enumerate(social_responses_db):
        if response.id == response_id:
            updated_response = SocialResponse(
                id=response_id,
                created_at=response.created_at,
                **response_update.dict()
            )
            social_responses_db[index] = updated_response
            return updated_response
    raise HTTPException(status_code=404, detail="Social response not found")

@router.delete("/responses/{response_id}")
def delete_social_response(response_id: int):
    """Delete a social response"""
    for index, response in enumerate(social_responses_db):
        if response.id == response_id:
            del social_responses_db[index]
            return {"message": "Social response deleted successfully"}
    raise HTTPException(status_code=404, detail="Social response not found")

@router.post("/responses/{response_id}/publish")
def publish_social_response(response_id: int):
    """Publish a social response"""
    for index, response in enumerate(social_responses_db):
        if response.id == response_id:
            social_responses_db[index].is_published = True
            social_responses_db[index].published_at = datetime.now()
            return {"message": "Social response published successfully"}
    raise HTTPException(status_code=404, detail="Social response not found")

@router.get("/inquiries/{inquiry_id}/responses", response_model=List[SocialResponse])
def get_responses_for_inquiry(inquiry_id: int):
    """Get responses for a specific social inquiry"""
    return [response for response in social_responses_db if response.inquiry_id == inquiry_id]

# Social Template endpoints
@router.get("/templates", response_model=List[SocialTemplate])
def list_social_templates():
    """List all social templates"""
    return social_templates_db

@router.get("/templates/{template_id}", response_model=SocialTemplate)
def get_social_template(template_id: int):
    """Get a specific social template by ID"""
    for template in social_templates_db:
        if template.id == template_id:
            return template
    raise HTTPException(status_code=404, detail="Social template not found")

@router.post("/templates", response_model=SocialTemplate)
def create_social_template(template: SocialTemplateCreate):
    """Create a new social template"""
    new_id = max([t.id for t in social_templates_db]) + 1 if social_templates_db else 1
    new_template = SocialTemplate(
        id=new_id,
        created_at=datetime.now(),
        **template.dict()
    )
    social_templates_db.append(new_template)
    return new_template

@router.put("/templates/{template_id}", response_model=SocialTemplate)
def update_social_template(template_id: int, template_update: SocialTemplateUpdate):
    """Update an existing social template"""
    for index, template in enumerate(social_templates_db):
        if template.id == template_id:
            updated_template = SocialTemplate(
                id=template_id,
                created_at=template.created_at,
                updated_at=datetime.now(),
                **template_update.dict()
            )
            social_templates_db[index] = updated_template
            return updated_template
    raise HTTPException(status_code=404, detail="Social template not found")

@router.delete("/templates/{template_id}")
def delete_social_template(template_id: int):
    """Delete a social template"""
    for index, template in enumerate(social_templates_db):
        if template.id == template_id:
            del social_templates_db[index]
            return {"message": "Social template deleted successfully"}
    raise HTTPException(status_code=404, detail="Social template not found")

@router.get("/templates/platform/{platform}", response_model=List[SocialTemplate])
def get_templates_by_platform(platform: str):
    """Get social templates by platform"""
    # Normalize the platform parameter to handle case differences
    normalized_platform = platform.lower().title()
    return [template for template in social_templates_db if template.platform.value == normalized_platform]

# Configuration endpoints
@router.get("/config/platforms", response_model=List[str])
def get_social_platform_options():
    """Get available social platform options"""
    return get_social_platforms()

@router.get("/config/sentiments", response_model=List[str])
def get_social_sentiment_options():
    """Get available social sentiment options"""
    return get_social_sentiments()