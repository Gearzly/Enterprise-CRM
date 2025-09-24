from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.support import Ticket as DBTicket, SLA as DBSLA
from .models import TicketCreate, TicketUpdate, SLACreate, SLAUpdate
from .config import get_ticket_priorities, get_ticket_statuses, get_ticket_channels
from fastapi import HTTPException

class TicketService:
    """Service class for handling ticket-related database operations"""
    
    def validate_ticket_data(self, ticket_data: dict):
        """Validate ticket data against dynamic configuration"""
        # Validate priority
        priorities = get_ticket_priorities()
        if 'priority' in ticket_data and ticket_data['priority'] not in priorities:
            raise HTTPException(status_code=400, detail=f"Invalid priority. Must be one of: {priorities}")
        
        # Validate status
        statuses = get_ticket_statuses()
        if 'status' in ticket_data and ticket_data['status'] not in statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {statuses}")
        
        # Validate channel
        channels = get_ticket_channels()
        if 'channel' in ticket_data and ticket_data['channel'] not in channels:
            raise HTTPException(status_code=400, detail=f"Invalid channel. Must be one of: {channels}")
    
    def get_tickets(self, db: Session) -> List[DBTicket]:
        """Get all tickets"""
        return db.query(DBTicket).all()
    
    def get_ticket(self, db: Session, ticket_id: int) -> Optional[DBTicket]:
        """Get a specific ticket by ID"""
        return db.query(DBTicket).filter(DBTicket.id == ticket_id).first()
    
    def create_ticket(self, db: Session, ticket: TicketCreate) -> DBTicket:
        """Create a new ticket"""
        # Validate ticket data
        ticket_data = ticket.dict()
        self.validate_ticket_data(ticket_data)
        
        db_ticket = DBTicket(**ticket_data)
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    def update_ticket(self, db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Optional[DBTicket]:
        """Update an existing ticket"""
        db_ticket = db.query(DBTicket).filter(DBTicket.id == ticket_id).first()
        if not db_ticket:
            return None
        
        # Validate ticket data
        update_data = ticket_update.dict(exclude_unset=True)
        self.validate_ticket_data(update_data)
        
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
        
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    def delete_ticket(self, db: Session, ticket_id: int) -> bool:
        """Delete a ticket"""
        db_ticket = db.query(DBTicket).filter(DBTicket.id == ticket_id).first()
        if not db_ticket:
            return False
        
        db.delete(db_ticket)
        db.commit()
        return True
    
    def get_tickets_by_priority(self, db: Session, priority: str) -> List[DBTicket]:
        """Get tickets by priority"""
        # Validate priority
        priorities = get_ticket_priorities()
        if priority not in priorities:
            raise HTTPException(status_code=400, detail=f"Invalid priority. Must be one of: {priorities}")
        
        return db.query(DBTicket).filter(DBTicket.priority == priority).all()
    
    def get_tickets_by_status(self, db: Session, status: str) -> List[DBTicket]:
        """Get tickets by status"""
        # Validate status
        statuses = get_ticket_statuses()
        if status not in statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {statuses}")
        
        return db.query(DBTicket).filter(DBTicket.status == status).all()
    
    def get_tickets_by_customer(self, db: Session, customer_id: int) -> List[DBTicket]:
        """Get tickets by customer ID"""
        return db.query(DBTicket).filter(DBTicket.customer_id == customer_id).all()

class SLAService:
    """Service class for handling SLA-related database operations"""
    
    def get_slas(self, db: Session) -> List[DBSLA]:
        """Get all SLAs"""
        return db.query(DBSLA).all()
    
    def get_sla(self, db: Session, sla_id: int) -> Optional[DBSLA]:
        """Get a specific SLA by ID"""
        return db.query(DBSLA).filter(DBSLA.id == sla_id).first()
    
    def create_sla(self, db: Session, sla: SLACreate) -> DBSLA:
        """Create a new SLA"""
        db_sla = DBSLA(**sla.dict())
        db.add(db_sla)
        db.commit()
        db.refresh(db_sla)
        return db_sla
    
    def update_sla(self, db: Session, sla_id: int, sla_update: SLAUpdate) -> Optional[DBSLA]:
        """Update an existing SLA"""
        db_sla = db.query(DBSLA).filter(DBSLA.id == sla_id).first()
        if not db_sla:
            return None
        
        for key, value in sla_update.dict(exclude_unset=True).items():
            setattr(db_sla, key, value)
        
        db.commit()
        db.refresh(db_sla)
        return db_sla
    
    def delete_sla(self, db: Session, sla_id: int) -> bool:
        """Delete an SLA"""
        db_sla = db.query(DBSLA).filter(DBSLA.id == sla_id).first()
        if not db_sla:
            return False
        
        db.delete(db_sla)
        db.commit()
        return True