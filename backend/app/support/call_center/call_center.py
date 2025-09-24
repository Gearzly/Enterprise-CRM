from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Call, CallCreate, CallUpdate,
    CallQueue, CallQueueCreate, CallQueueUpdate,
    IVRMenu, IVRMenuCreate, IVRMenuUpdate
)
from .config import (
    get_call_directions, get_call_statuses, 
    get_call_priorities, get_default_priority, get_max_wait_time_minutes
)

router = APIRouter(prefix="/call-center", tags=["call-center"])

# In-memory storage for demo purposes
calls_db = []
call_queues_db = []
ivr_menus_db = []

@router.get("/")
def get_call_center_dashboard():
    """Get support call center dashboard with summary statistics"""
    return {
        "message": "Support Call Center Dashboard",
        "statistics": {
            "total_calls": len(calls_db),
            "total_queues": len(call_queues_db),
            "total_ivr_menus": len(ivr_menus_db),
            "active_calls": len([c for c in calls_db if c.status == "In Progress"])
        }
    }

@router.get("/calls", response_model=List[Call])
def list_calls():
    """List all calls"""
    return calls_db

@router.get("/calls/{call_id}", response_model=Call)
def get_call(call_id: int):
    """Get a specific call by ID"""
    for call in calls_db:
        if call.id == call_id:
            return call
    raise HTTPException(status_code=404, detail="Call not found")

@router.post("/calls", response_model=Call)
def create_call(call: CallCreate):
    """Create a new call"""
    new_id = max([c.id for c in calls_db]) + 1 if calls_db else 1
    new_call = Call(
        id=new_id,
        created_at=datetime.now(),
        **call.dict()
    )
    calls_db.append(new_call)
    return new_call

@router.put("/calls/{call_id}", response_model=Call)
def update_call(call_id: int, call_update: CallUpdate):
    """Update an existing call"""
    for index, call in enumerate(calls_db):
        if call.id == call_id:
            updated_call = Call(
                id=call_id,
                created_at=call.created_at,
                updated_at=datetime.now(),
                **call_update.dict()
            )
            calls_db[index] = updated_call
            return updated_call
    raise HTTPException(status_code=404, detail="Call not found")

@router.delete("/calls/{call_id}")
def delete_call(call_id: int):
    """Delete a call"""
    for index, call in enumerate(calls_db):
        if call.id == call_id:
            del calls_db[index]
            return {"message": "Call deleted successfully"}
    raise HTTPException(status_code=404, detail="Call not found")

@router.post("/calls/{call_id}/answer")
def answer_call(call_id: int, agent_id: str):
    """Answer a call"""
    for index, call in enumerate(calls_db):
        if call.id == call_id:
            calls_db[index].status = "In Progress"
            calls_db[index].assigned_agent_id = agent_id
            calls_db[index].answered_at = datetime.now()
            return {"message": "Call answered successfully"}
    raise HTTPException(status_code=404, detail="Call not found")

@router.post("/calls/{call_id}/end")
def end_call(call_id: int, duration_seconds: Optional[int] = None):
    """End a call"""
    for index, call in enumerate(calls_db):
        if call.id == call_id:
            calls_db[index].status = "Completed"
            calls_db[index].ended_at = datetime.now()
            if duration_seconds is not None:
                calls_db[index].duration_seconds = duration_seconds
            return {"message": "Call ended successfully"}
    raise HTTPException(status_code=404, detail="Call not found")

@router.get("/calls/customer/{customer_id}", response_model=List[Call])
def get_calls_by_customer(customer_id: int):
    """Get calls by customer ID"""
    return [call for call in calls_db if call.customer_id == customer_id]

@router.get("/calls/agent/{agent_id}", response_model=List[Call])
def get_calls_by_agent(agent_id: str):
    """Get calls by agent ID"""
    return [call for call in calls_db if call.assigned_agent_id == agent_id]

@router.get("/calls/status/{status}", response_model=List[Call])
def get_calls_by_status(status: str):
    """Get calls by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [call for call in calls_db if call.status == normalized_status]

@router.get("/calls/direction/{direction}", response_model=List[Call])
def get_calls_by_direction(direction: str):
    """Get calls by direction"""
    # Normalize the direction parameter to handle case differences
    normalized_direction = direction.lower().title()
    return [call for call in calls_db if call.direction == normalized_direction]

# Call Queue endpoints
@router.get("/queues", response_model=List[CallQueue])
def list_call_queues():
    """List all call queues"""
    return call_queues_db

@router.get("/queues/{queue_id}", response_model=CallQueue)
def get_call_queue(queue_id: int):
    """Get a specific call queue by ID"""
    for queue in call_queues_db:
        if queue.id == queue_id:
            return queue
    raise HTTPException(status_code=404, detail="Call queue not found")

@router.post("/queues", response_model=CallQueue)
def create_call_queue(queue: CallQueueCreate):
    """Create a new call queue"""
    new_id = max([q.id for q in call_queues_db]) + 1 if call_queues_db else 1
    new_queue = CallQueue(
        id=new_id,
        created_at=datetime.now(),
        **queue.dict()
    )
    call_queues_db.append(new_queue)
    return new_queue

@router.put("/queues/{queue_id}", response_model=CallQueue)
def update_call_queue(queue_id: int, queue_update: CallQueueUpdate):
    """Update an existing call queue"""
    for index, queue in enumerate(call_queues_db):
        if queue.id == queue_id:
            updated_queue = CallQueue(
                id=queue_id,
                created_at=queue.created_at,
                updated_at=datetime.now(),
                **queue_update.dict()
            )
            call_queues_db[index] = updated_queue
            return updated_queue
    raise HTTPException(status_code=404, detail="Call queue not found")

@router.delete("/queues/{queue_id}")
def delete_call_queue(queue_id: int):
    """Delete a call queue"""
    for index, queue in enumerate(call_queues_db):
        if queue.id == queue_id:
            del call_queues_db[index]
            return {"message": "Call queue deleted successfully"}
    raise HTTPException(status_code=404, detail="Call queue not found")

# IVR Menu endpoints
@router.get("/ivr", response_model=List[IVRMenu])
def list_ivr_menus():
    """List all IVR menus"""
    return ivr_menus_db

@router.get("/ivr/{menu_id}", response_model=IVRMenu)
def get_ivr_menu(menu_id: int):
    """Get a specific IVR menu by ID"""
    for menu in ivr_menus_db:
        if menu.id == menu_id:
            return menu
    raise HTTPException(status_code=404, detail="IVR menu not found")

@router.post("/ivr", response_model=IVRMenu)
def create_ivr_menu(menu: IVRMenuCreate):
    """Create a new IVR menu"""
    new_id = max([m.id for m in ivr_menus_db]) + 1 if ivr_menus_db else 1
    new_menu = IVRMenu(
        id=new_id,
        created_at=datetime.now(),
        **menu.dict()
    )
    ivr_menus_db.append(new_menu)
    return new_menu

@router.put("/ivr/{menu_id}", response_model=IVRMenu)
def update_ivr_menu(menu_id: int, menu_update: IVRMenuUpdate):
    """Update an existing IVR menu"""
    for index, menu in enumerate(ivr_menus_db):
        if menu.id == menu_id:
            updated_menu = IVRMenu(
                id=menu_id,
                created_at=menu.created_at,
                updated_at=datetime.now(),
                **menu_update.dict()
            )
            ivr_menus_db[index] = updated_menu
            return updated_menu
    raise HTTPException(status_code=404, detail="IVR menu not found")

@router.delete("/ivr/{menu_id}")
def delete_ivr_menu(menu_id: int):
    """Delete an IVR menu"""
    for index, menu in enumerate(ivr_menus_db):
        if menu.id == menu_id:
            del ivr_menus_db[index]
            return {"message": "IVR menu deleted successfully"}
    raise HTTPException(status_code=404, detail="IVR menu not found")

# Configuration endpoints
@router.get("/config/directions", response_model=List[str])
def get_call_direction_options():
    """Get available call direction options"""
    return get_call_directions()

@router.get("/config/statuses", response_model=List[str])
def get_call_status_options():
    """Get available call status options"""
    return get_call_statuses()

@router.get("/config/priorities", response_model=List[str])
def get_call_priority_options():
    """Get available call priority options"""
    return get_call_priorities()