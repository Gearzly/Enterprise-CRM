from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.marketing import Campaign as DBCampaign, CampaignTemplate as DBCampaignTemplate, ABTest as DBABTest
from .models import CampaignCreate, CampaignUpdate, CampaignTemplateCreate, CampaignTemplateUpdate, ABTestCreate, ABTestUpdate
from .config import get_campaign_statuses, get_campaign_types, get_ab_test_metrics
from fastapi import HTTPException

class CampaignService:
    """Service class for handling campaign-related database operations"""
    
    def validate_campaign_data(self, campaign_data: dict):
        """Validate campaign data against dynamic configuration"""
        # Validate status
        statuses = get_campaign_statuses()
        if 'status' in campaign_data and campaign_data['status'] not in statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {statuses}")
        
        # Validate type
        types = get_campaign_types()
        if 'type' in campaign_data and campaign_data['type'] not in types:
            raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {types}")
    
    def get_campaigns(self, db: Session) -> List[DBCampaign]:
        """Get all campaigns"""
        return db.query(DBCampaign).all()
    
    def get_campaign(self, db: Session, campaign_id: int) -> Optional[DBCampaign]:
        """Get a specific campaign by ID"""
        return db.query(DBCampaign).filter(DBCampaign.id == campaign_id).first()
    
    def create_campaign(self, db: Session, campaign: CampaignCreate) -> DBCampaign:
        """Create a new campaign"""
        # Validate campaign data
        campaign_data = campaign.dict()
        self.validate_campaign_data(campaign_data)
        
        db_campaign = DBCampaign(**campaign_data)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    
    def update_campaign(self, db: Session, campaign_id: int, campaign_update: CampaignUpdate) -> Optional[DBCampaign]:
        """Update an existing campaign"""
        db_campaign = db.query(DBCampaign).filter(DBCampaign.id == campaign_id).first()
        if not db_campaign:
            return None
        
        # Validate campaign data
        update_data = campaign_update.dict(exclude_unset=True)
        self.validate_campaign_data(update_data)
        
        for key, value in update_data.items():
            setattr(db_campaign, key, value)
        
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    
    def delete_campaign(self, db: Session, campaign_id: int) -> bool:
        """Delete a campaign"""
        db_campaign = db.query(DBCampaign).filter(DBCampaign.id == campaign_id).first()
        if not db_campaign:
            return False
        
        db.delete(db_campaign)
        db.commit()
        return True
    
    def get_campaigns_by_status(self, db: Session, status: str) -> List[DBCampaign]:
        """Get campaigns by status"""
        # Validate status
        statuses = get_campaign_statuses()
        if status not in statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {statuses}")
        
        return db.query(DBCampaign).filter(DBCampaign.status == status).all()
    
    def get_campaigns_by_type(self, db: Session, campaign_type: str) -> List[DBCampaign]:
        """Get campaigns by type"""
        # Validate type
        types = get_campaign_types()
        if campaign_type not in types:
            raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {types}")
        
        return db.query(DBCampaign).filter(DBCampaign.type == campaign_type).all()

class CampaignTemplateService:
    """Service class for handling campaign template-related database operations"""
    
    def validate_template_data(self, template_data: dict):
        """Validate template data against dynamic configuration"""
        # Validate type
        types = get_campaign_types()
        if 'type' in template_data and template_data['type'] not in types:
            raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {types}")
    
    def get_templates(self, db: Session) -> List[DBCampaignTemplate]:
        """Get all campaign templates"""
        return db.query(DBCampaignTemplate).all()
    
    def get_template(self, db: Session, template_id: int) -> Optional[DBCampaignTemplate]:
        """Get a specific campaign template by ID"""
        return db.query(DBCampaignTemplate).filter(DBCampaignTemplate.id == template_id).first()
    
    def create_template(self, db: Session, template: CampaignTemplateCreate) -> DBCampaignTemplate:
        """Create a new campaign template"""
        # Validate template data
        template_data = template.dict()
        self.validate_template_data(template_data)
        
        db_template = DBCampaignTemplate(**template_data)
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template
    
    def update_template(self, db: Session, template_id: int, template_update: CampaignTemplateUpdate) -> Optional[DBCampaignTemplate]:
        """Update an existing campaign template"""
        db_template = db.query(DBCampaignTemplate).filter(DBCampaignTemplate.id == template_id).first()
        if not db_template:
            return None
        
        # Validate template data
        update_data = template_update.dict(exclude_unset=True)
        self.validate_template_data(update_data)
        
        for key, value in update_data.items():
            setattr(db_template, key, value)
        
        db.commit()
        db.refresh(db_template)
        return db_template
    
    def delete_template(self, db: Session, template_id: int) -> bool:
        """Delete a campaign template"""
        db_template = db.query(DBCampaignTemplate).filter(DBCampaignTemplate.id == template_id).first()
        if not db_template:
            return False
        
        db.delete(db_template)
        db.commit()
        return True

class ABTestService:
    """Service class for handling A/B test-related database operations"""
    
    def validate_ab_test_data(self, test_data: dict):
        """Validate A/B test data against dynamic configuration"""
        # Validate test metric
        metrics = get_ab_test_metrics()
        if 'test_metric' in test_data and test_data['test_metric'] not in metrics:
            raise HTTPException(status_code=400, detail=f"Invalid test metric. Must be one of: {metrics}")
    
    def get_ab_tests(self, db: Session) -> List[DBABTest]:
        """Get all A/B tests"""
        return db.query(DBABTest).all()
    
    def get_ab_test(self, db: Session, test_id: int) -> Optional[DBABTest]:
        """Get a specific A/B test by ID"""
        return db.query(DBABTest).filter(DBABTest.id == test_id).first()
    
    def create_ab_test(self, db: Session, test: ABTestCreate) -> DBABTest:
        """Create a new A/B test"""
        # Validate A/B test data
        test_data = test.dict()
        self.validate_ab_test_data(test_data)
        
        db_test = DBABTest(**test_data)
        db.add(db_test)
        db.commit()
        db.refresh(db_test)
        return db_test
    
    def update_ab_test(self, db: Session, test_id: int, test_update: ABTestUpdate) -> Optional[DBABTest]:
        """Update an existing A/B test"""
        db_test = db.query(DBABTest).filter(DBABTest.id == test_id).first()
        if not db_test:
            return None
        
        # Validate A/B test data
        update_data = test_update.dict(exclude_unset=True)
        self.validate_ab_test_data(update_data)
        
        for key, value in update_data.items():
            setattr(db_test, key, value)
        
        db.commit()
        db.refresh(db_test)
        return db_test
    
    def delete_ab_test(self, db: Session, test_id: int) -> bool:
        """Delete an A/B test"""
        db_test = db.query(DBABTest).filter(DBABTest.id == test_id).first()
        if not db_test:
            return False
        
        db.delete(db_test)
        db.commit()
        return True