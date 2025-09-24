from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .models import (
    Ticket, TicketCreate, TicketUpdate,
    SLA, SLACreate, SLAUpdate
)
from .config import (
    get_ticket_priorities, get_ticket_statuses, 
    get_ticket_channels
)
from .service import TicketService, SLAService
from app.core.database import get_db

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Initialize services
ticket_service = TicketService()
sla_service = SLAService()

@router.get("/")
def get_tickets_dashboard():
    """Get support tickets dashboard with summary statistics"""
    return {
        "message": "Support Tickets Dashboard",
        "statistics": {
            "total_tickets": "Available via list endpoint",
            "tickets_by_priority": "Filtered by priority",
            "tickets_by_status": "Filtered by status",
            "slas": "Available via slas endpoint"
        }
    }

@router.get("/tickets", response_model=List[Ticket])
def list_tickets(db: Session = Depends(get_db)):
    """List all tickets"""
    return ticket_service.get_tickets(db)

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get a specific ticket by ID"""
    ticket = ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/", response_model=Ticket)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket"""
    return ticket_service.create_ticket(db, ticket)

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    """Update an existing ticket"""
    ticket = ticket_service.update_ticket(db, ticket_id, ticket_update)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Delete a ticket"""
    success = ticket_service.delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}

@router.get("/priority/{priority}", response_model=List[Ticket])
def get_tickets_by_priority(priority: str, db: Session = Depends(get_db)):
    """Get tickets by priority"""
    return ticket_service.get_tickets_by_priority(db, priority)

@router.get("/status/{status}", response_model=List[Ticket])
def get_tickets_by_status(status: str, db: Session = Depends(get_db)):
    """Get tickets by status"""
    return ticket_service.get_tickets_by_status(db, status)

@router.get("/customer/{customer_id}", response_model=List[Ticket])
def get_tickets_by_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get tickets by customer ID"""
    return ticket_service.get_tickets_by_customer(db, customer_id)

# SLA endpoints
@router.get("/slas", response_model=List[SLA])
def list_slas(db: Session = Depends(get_db)):
    """List all SLAs"""
    return sla_service.get_slas(db)

@router.get("/slas/{sla_id}", response_model=SLA)
def get_sla(sla_id: int, db: Session = Depends(get_db)):
    """Get a specific SLA by ID"""
    sla = sla_service.get_sla(db, sla_id)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return sla

@router.post("/slas", response_model=SLA)
def create_sla(sla: SLACreate, db: Session = Depends(get_db)):
    """Create a new SLA"""
    return sla_service.create_sla(db, sla)

@router.put("/slas/{sla_id}", response_model=SLA)
def update_sla(sla_id: int, sla_update: SLAUpdate, db: Session = Depends(get_db)):
    """Update an existing SLA"""
    sla = sla_service.update_sla(db, sla_id, sla_update)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return sla

@router.delete("/slas/{sla_id}")
def delete_sla(sla_id: int, db: Session = Depends(get_db)):
    """Delete an SLA"""
    success = sla_service.delete_sla(db, sla_id)
    if not success:
        raise HTTPException(status_code=404, detail="SLA not found")
    return {"message": "SLA deleted successfully"}

# Configuration endpoints
@router.get("/config/priorities", response_model=List[str])
def get_ticket_priority_options():
    """Get available ticket priority options"""
    return get_ticket_priorities()

@router.get("/config/statuses", response_model=List[str])
def get_ticket_status_options():
    """Get available ticket status options"""
    return get_ticket_statuses()

@router.get("/config/channels", response_model=List[str])
def get_ticket_channel_options():
    """Get available ticket channel options"""
    return get_ticket_channels()