from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Ticket, TicketCreate, TicketUpdate,
    SLA, SLACreate, SLAUpdate
)
from .config import (
    get_ticket_priorities, get_ticket_statuses, 
    get_ticket_channels, get_default_priority, get_default_status
)

router = APIRouter()

# In-memory storage for demo purposes
tickets_db = []
slas_db = []

@router.get("/", response_model=List[Ticket])
def list_tickets():
    """List all tickets"""
    return tickets_db

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    """Get a specific ticket by ID"""
    for ticket in tickets_db:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@router.post("/", response_model=Ticket)
def create_ticket(ticket: TicketCreate):
    """Create a new ticket"""
    new_id = max([t.id for t in tickets_db]) + 1 if tickets_db else 1
    new_ticket = Ticket(
        id=new_id,
        created_at=datetime.now(),
        **ticket.dict()
    )
    tickets_db.append(new_ticket)
    return new_ticket

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket_update: TicketUpdate):
    """Update an existing ticket"""
    for index, ticket in enumerate(tickets_db):
        if ticket.id == ticket_id:
            updated_ticket = Ticket(
                id=ticket_id,
                created_at=ticket.created_at,
                updated_at=datetime.now(),
                **ticket_update.dict()
            )
            tickets_db[index] = updated_ticket
            return updated_ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    """Delete a ticket"""
    for index, ticket in enumerate(tickets_db):
        if ticket.id == ticket_id:
            del tickets_db[index]
            return {"message": "Ticket deleted successfully"}
    raise HTTPException(status_code=404, detail="Ticket not found")

@router.get("/priority/{priority}", response_model=List[Ticket])
def get_tickets_by_priority(priority: str):
    """Get tickets by priority"""
    # Normalize the priority parameter to handle case differences
    normalized_priority = priority.lower().title()
    return [ticket for ticket in tickets_db if ticket.priority.value == normalized_priority]

@router.get("/status/{status}", response_model=List[Ticket])
def get_tickets_by_status(status: str):
    """Get tickets by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title().replace("_", " ")
    return [ticket for ticket in tickets_db if ticket.status.value == normalized_status]

@router.get("/customer/{customer_id}", response_model=List[Ticket])
def get_tickets_by_customer(customer_id: int):
    """Get tickets by customer ID"""
    return [ticket for ticket in tickets_db if ticket.customer_id == customer_id]

# SLA endpoints
@router.get("/slas", response_model=List[SLA])
def list_slas():
    """List all SLAs"""
    return slas_db

@router.get("/slas/{sla_id}", response_model=SLA)
def get_sla(sla_id: int):
    """Get a specific SLA by ID"""
    for sla in slas_db:
        if sla.id == sla_id:
            return sla
    raise HTTPException(status_code=404, detail="SLA not found")

@router.post("/slas", response_model=SLA)
def create_sla(sla: SLACreate):
    """Create a new SLA"""
    new_id = max([s.id for s in slas_db]) + 1 if slas_db else 1
    new_sla = SLA(
        id=new_id,
        created_at=datetime.now(),
        **sla.dict()
    )
    slas_db.append(new_sla)
    return new_sla

@router.put("/slas/{sla_id}", response_model=SLA)
def update_sla(sla_id: int, sla_update: SLAUpdate):
    """Update an existing SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            updated_sla = SLA(
                id=sla_id,
                created_at=sla.created_at,
                updated_at=datetime.now(),
                **sla_update.dict()
            )
            slas_db[index] = updated_sla
            return updated_sla
    raise HTTPException(status_code=404, detail="SLA not found")

@router.delete("/slas/{sla_id}")
def delete_sla(sla_id: int):
    """Delete an SLA"""
    for index, sla in enumerate(slas_db):
        if sla.id == sla_id:
            del slas_db[index]
            return {"message": "SLA deleted successfully"}
    raise HTTPException(status_code=404, detail="SLA not found")

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