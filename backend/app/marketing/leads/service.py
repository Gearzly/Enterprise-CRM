from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .models import (
    Lead, LeadCreate, LeadUpdate,
    LeadForm, LeadFormCreate, LeadFormUpdate,
    LeadScoreRule, LeadScoreRuleCreate, LeadScoreRuleUpdate,
    LeadAssignmentRule, LeadAssignmentRuleCreate, LeadAssignmentRuleUpdate
)
from app.models.marketing import (
    Lead as DBLead,
    LeadForm as DBLeadForm,
    LeadScoreRule as DBLeadScoreRule,
    LeadAssignmentRule as DBLeadAssignmentRule
)

class LeadService:
    """Service class for handling lead operations"""
    
    def get_leads(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBLead]:
        """Get all leads"""
        return db.query(DBLead).offset(skip).limit(limit).all()
    
    def get_lead(self, db: Session, lead_id: int) -> Optional[DBLead]:
        """Get a specific lead by ID"""
        return db.query(DBLead).filter(DBLead.id == lead_id).first()
    
    def create_lead(self, db: Session, lead: LeadCreate) -> DBLead:
        """Create a new lead"""
        db_lead = DBLead(**lead.dict())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    
    def update_lead(self, db: Session, lead_id: int, lead_update: LeadUpdate) -> Optional[DBLead]:
        """Update an existing lead"""
        db_lead = self.get_lead(db, lead_id)
        if db_lead:
            update_data = lead_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_lead, key, value)
            db.commit()
            db.refresh(db_lead)
        return db_lead
    
    def delete_lead(self, db: Session, lead_id: int) -> bool:
        """Delete a lead"""
        db_lead = self.get_lead(db, lead_id)
        if db_lead:
            db.delete(db_lead)
            db.commit()
            return True
        return False
    
    def get_leads_by_status(self, db: Session, status: str) -> List[DBLead]:
        """Get leads by status"""
        return db.query(DBLead).filter(DBLead.status == status).all()
    
    def get_leads_by_source(self, db: Session, source: str) -> List[DBLead]:
        """Get leads by source"""
        return db.query(DBLead).filter(DBLead.source == source).all()
    
    def get_leads_by_score_range(self, db: Session, min_score: int, max_score: int) -> List[DBLead]:
        """Get leads by score range"""
        return db.query(DBLead).filter(DBLead.score >= min_score, DBLead.score <= max_score).all()


class LeadFormService:
    """Service class for handling lead form operations"""
    
    def get_forms(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBLeadForm]:
        """Get all lead forms"""
        return db.query(DBLeadForm).offset(skip).limit(limit).all()
    
    def get_form(self, db: Session, form_id: int) -> Optional[DBLeadForm]:
        """Get a specific lead form by ID"""
        return db.query(DBLeadForm).filter(DBLeadForm.id == form_id).first()
    
    def create_form(self, db: Session, form: LeadFormCreate) -> DBLeadForm:
        """Create a new lead form"""
        db_form = DBLeadForm(**form.dict())
        db.add(db_form)
        db.commit()
        db.refresh(db_form)
        return db_form
    
    def update_form(self, db: Session, form_id: int, form_update: LeadFormUpdate) -> Optional[DBLeadForm]:
        """Update an existing lead form"""
        db_form = self.get_form(db, form_id)
        if db_form:
            update_data = form_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_form, key, value)
            db.commit()
            db.refresh(db_form)
        return db_form
    
    def delete_form(self, db: Session, form_id: int) -> bool:
        """Delete a lead form"""
        db_form = self.get_form(db, form_id)
        if db_form:
            db.delete(db_form)
            db.commit()
            return True
        return False


class LeadScoreRuleService:
    """Service class for handling lead scoring rule operations"""
    
    def get_rules(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBLeadScoreRule]:
        """Get all lead scoring rules"""
        return db.query(DBLeadScoreRule).offset(skip).limit(limit).all()
    
    def get_rule(self, db: Session, rule_id: int) -> Optional[DBLeadScoreRule]:
        """Get a specific lead scoring rule by ID"""
        return db.query(DBLeadScoreRule).filter(DBLeadScoreRule.id == rule_id).first()
    
    def create_rule(self, db: Session, rule: LeadScoreRuleCreate) -> DBLeadScoreRule:
        """Create a new lead scoring rule"""
        db_rule = DBLeadScoreRule(**rule.dict())
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule
    
    def update_rule(self, db: Session, rule_id: int, rule_update: LeadScoreRuleUpdate) -> Optional[DBLeadScoreRule]:
        """Update an existing lead scoring rule"""
        db_rule = self.get_rule(db, rule_id)
        if db_rule:
            update_data = rule_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_rule, key, value)
            db.commit()
            db.refresh(db_rule)
        return db_rule
    
    def delete_rule(self, db: Session, rule_id: int) -> bool:
        """Delete a lead scoring rule"""
        db_rule = self.get_rule(db, rule_id)
        if db_rule:
            db.delete(db_rule)
            db.commit()
            return True
        return False


class LeadAssignmentRuleService:
    """Service class for handling lead assignment rule operations"""
    
    def get_rules(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBLeadAssignmentRule]:
        """Get all lead assignment rules"""
        return db.query(DBLeadAssignmentRule).offset(skip).limit(limit).all()
    
    def get_rule(self, db: Session, rule_id: int) -> Optional[DBLeadAssignmentRule]:
        """Get a specific lead assignment rule by ID"""
        return db.query(DBLeadAssignmentRule).filter(DBLeadAssignmentRule.id == rule_id).first()
    
    def create_rule(self, db: Session, rule: LeadAssignmentRuleCreate) -> DBLeadAssignmentRule:
        """Create a new lead assignment rule"""
        db_rule = DBLeadAssignmentRule(**rule.dict())
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule
    
    def update_rule(self, db: Session, rule_id: int, rule_update: LeadAssignmentRuleUpdate) -> Optional[DBLeadAssignmentRule]:
        """Update an existing lead assignment rule"""
        db_rule = self.get_rule(db, rule_id)
        if db_rule:
            update_data = rule_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_rule, key, value)
            db.commit()
            db.refresh(db_rule)
        return db_rule
    
    def delete_rule(self, db: Session, rule_id: int) -> bool:
        """Delete a lead assignment rule"""
        db_rule = self.get_rule(db, rule_id)
        if db_rule:
            db.delete(db_rule)
            db.commit()
            return True
        return False