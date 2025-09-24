from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Interaction, InteractionCreate, InteractionUpdate,
    InteractionNote, InteractionNoteCreate
)
from .config import (
    get_interaction_types, get_default_interaction_type, get_max_tags_per_interaction
)

router = APIRouter(prefix="/interactions", tags=["interactions"])

# In-memory storage for demo purposes
interactions_db = []
interaction_notes_db = []

@router.get("/")
def get_interactions_dashboard():
    """Get support interactions dashboard with summary statistics"""
    return {
        "message": "Support Interactions Dashboard",
        "statistics": {
            "total_interactions": len(interactions_db),
            "interactions_by_type": "Filtered by type",
            "interactions_by_agent": "Filtered by agent",
            "recent_interactions": "Available via customer endpoints"
        }
    }

@router.get("/interactions", response_model=List[Interaction])
def list_interactions():
    """List all interactions"""
    return interactions_db

@router.get("/{interaction_id}", response_model=Interaction)
def get_interaction(interaction_id: int):
    """Get a specific interaction by ID"""
    for interaction in interactions_db:
        if interaction.id == interaction_id:
            return interaction
    raise HTTPException(status_code=404, detail="Interaction not found")

@router.post("/", response_model=Interaction)
def create_interaction(interaction: InteractionCreate):
    """Create a new interaction"""
    new_id = max([i.id for i in interactions_db]) + 1 if interactions_db else 1
    new_interaction = Interaction(
        id=new_id,
        created_at=datetime.now(),
        **interaction.dict()
    )
    interactions_db.append(new_interaction)
    return new_interaction

@router.put("/{interaction_id}", response_model=Interaction)
def update_interaction(interaction_id: int, interaction_update: InteractionUpdate):
    """Update an existing interaction"""
    for index, interaction in enumerate(interactions_db):
        if interaction.id == interaction_id:
            updated_interaction = Interaction(
                id=interaction_id,
                created_at=interaction.created_at,
                updated_at=datetime.now(),
                **interaction_update.dict()
            )
            interactions_db[index] = updated_interaction
            return updated_interaction
    raise HTTPException(status_code=404, detail="Interaction not found")

@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int):
    """Delete an interaction"""
    for index, interaction in enumerate(interactions_db):
        if interaction.id == interaction_id:
            del interactions_db[index]
            return {"message": "Interaction deleted successfully"}
    raise HTTPException(status_code=404, detail="Interaction not found")

@router.get("/customer/{customer_id}", response_model=List[Interaction])
def get_interactions_by_customer(customer_id: int):
    """Get interactions by customer ID"""
    return [interaction for interaction in interactions_db if interaction.customer_id == customer_id]

@router.get("/type/{type}", response_model=List[Interaction])
def get_interactions_by_type(type: str):
    """Get interactions by type"""
    # Normalize the type parameter to handle case differences
    normalized_type = type.lower().title()
    return [interaction for interaction in interactions_db if interaction.type == normalized_type]

@router.get("/agent/{agent_id}", response_model=List[Interaction])
def get_interactions_by_agent(agent_id: str):
    """Get interactions by agent ID"""
    return [interaction for interaction in interactions_db if interaction.agent_id == agent_id]

# Interaction Notes endpoints
@router.get("/notes", response_model=List[InteractionNote])
def list_interaction_notes():
    """List all interaction notes"""
    return interaction_notes_db

@router.get("/notes/{note_id}", response_model=InteractionNote)
def get_interaction_note(note_id: int):
    """Get a specific interaction note by ID"""
    for note in interaction_notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Interaction note not found")

@router.post("/notes", response_model=InteractionNote)
def create_interaction_note(note: InteractionNoteCreate):
    """Create a new interaction note"""
    new_id = max([n.id for n in interaction_notes_db]) + 1 if interaction_notes_db else 1
    new_note = InteractionNote(
        id=new_id,
        created_at=datetime.now(),
        **note.dict()
    )
    interaction_notes_db.append(new_note)
    return new_note

@router.put("/notes/{note_id}", response_model=InteractionNote)
def update_interaction_note(note_id: int, note_update: InteractionNoteCreate):
    """Update an existing interaction note"""
    for index, note in enumerate(interaction_notes_db):
        if note.id == note_id:
            updated_note = InteractionNote(
                id=note_id,
                created_at=note.created_at,
                **note_update.dict()
            )
            interaction_notes_db[index] = updated_note
            return updated_note
    raise HTTPException(status_code=404, detail="Interaction note not found")

@router.delete("/notes/{note_id}")
def delete_interaction_note(note_id: int):
    """Delete an interaction note"""
    for index, note in enumerate(interaction_notes_db):
        if note.id == note_id:
            del interaction_notes_db[index]
            return {"message": "Interaction note deleted successfully"}
    raise HTTPException(status_code=404, detail="Interaction note not found")

@router.get("/{interaction_id}/notes", response_model=List[InteractionNote])
def get_notes_for_interaction(interaction_id: int):
    """Get notes for a specific interaction"""
    return [note for note in interaction_notes_db if note.interaction_id == interaction_id]

# Configuration endpoints
@router.get("/config/types", response_model=List[str])
def get_interaction_type_options():
    """Get available interaction type options"""
    return get_interaction_types()