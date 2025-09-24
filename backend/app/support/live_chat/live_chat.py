from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    ChatSession, ChatSessionCreate, ChatSessionUpdate,
    ChatMessage, ChatMessageCreate,
    ChatTranscript, ChatTranscriptCreate
)
from .config import (
    get_chat_statuses, get_chat_priorities, 
    get_default_priority, get_max_message_length
)

router = APIRouter(prefix="/live-chat", tags=["live-chat"])

# In-memory storage for demo purposes
chat_sessions_db = []
chat_messages_db = []
chat_transcripts_db = []

@router.get("/")
def get_live_chat_dashboard():
    """Get support live chat dashboard with summary statistics"""
    return {
        "message": "Support Live Chat Dashboard",
        "statistics": {
            "total_sessions": len(chat_sessions_db),
            "total_messages": len(chat_messages_db),
            "total_transcripts": len(chat_transcripts_db),
            "active_sessions": len([s for s in chat_sessions_db if s.status == "Active"])
        }
    }

@router.get("/sessions", response_model=List[ChatSession])
def list_chat_sessions():
    """List all chat sessions"""
    return chat_sessions_db

@router.get("/sessions/{session_id}", response_model=ChatSession)
def get_chat_session(session_id: int):
    """Get a specific chat session by ID"""
    for session in chat_sessions_db:
        if session.id == session_id:
            return session
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.post("/sessions", response_model=ChatSession)
def create_chat_session(session: ChatSessionCreate):
    """Create a new chat session"""
    new_id = max([s.id for s in chat_sessions_db]) + 1 if chat_sessions_db else 1
    new_session = ChatSession(
        id=new_id,
        created_at=datetime.now(),
        **session.dict()
    )
    chat_sessions_db.append(new_session)
    return new_session

@router.put("/sessions/{session_id}", response_model=ChatSession)
def update_chat_session(session_id: int, session_update: ChatSessionUpdate):
    """Update an existing chat session"""
    for index, session in enumerate(chat_sessions_db):
        if session.id == session_id:
            updated_session = ChatSession(
                id=session_id,
                created_at=session.created_at,
                updated_at=datetime.now(),
                **session_update.dict()
            )
            chat_sessions_db[index] = updated_session
            return updated_session
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.delete("/sessions/{session_id}")
def delete_chat_session(session_id: int):
    """Delete a chat session"""
    for index, session in enumerate(chat_sessions_db):
        if session.id == session_id:
            del chat_sessions_db[index]
            return {"message": "Chat session deleted successfully"}
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.post("/sessions/{session_id}/accept")
def accept_chat_session(session_id: int, agent_id: str):
    """Accept a chat session"""
    for index, session in enumerate(chat_sessions_db):
        if session.id == session_id:
            chat_sessions_db[index].status = "Active"
            chat_sessions_db[index].assigned_agent_id = agent_id
            chat_sessions_db[index].accepted_at = datetime.now()
            return {"message": "Chat session accepted successfully"}
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.post("/sessions/{session_id}/close")
def close_chat_session(session_id: int):
    """Close a chat session"""
    for index, session in enumerate(chat_sessions_db):
        if session.id == session_id:
            chat_sessions_db[index].status = "Closed"
            chat_sessions_db[index].closed_at = datetime.now()
            return {"message": "Chat session closed successfully"}
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.post("/sessions/{session_id}/transfer")
def transfer_chat_session(session_id: int, new_agent_id: str):
    """Transfer a chat session to another agent"""
    for index, session in enumerate(chat_sessions_db):
        if session.id == session_id:
            chat_sessions_db[index].status = "Transferred"
            chat_sessions_db[index].assigned_agent_id = new_agent_id
            return {"message": "Chat session transferred successfully"}
    raise HTTPException(status_code=404, detail="Chat session not found")

@router.get("/sessions/customer/{customer_id}", response_model=List[ChatSession])
def get_chat_sessions_by_customer(customer_id: int):
    """Get chat sessions by customer ID"""
    return [session for session in chat_sessions_db if session.customer_id == customer_id]

@router.get("/sessions/agent/{agent_id}", response_model=List[ChatSession])
def get_chat_sessions_by_agent(agent_id: str):
    """Get chat sessions by agent ID"""
    return [session for session in chat_sessions_db if session.assigned_agent_id == agent_id]

@router.get("/sessions/status/{status}", response_model=List[ChatSession])
def get_chat_sessions_by_status(status: str):
    """Get chat sessions by status"""
    # Normalize the status parameter to handle case differences
    normalized_status = status.lower().title()
    return [session for session in chat_sessions_db if session.status == normalized_status]

# Chat Messages endpoints
@router.get("/messages", response_model=List[ChatMessage])
def list_chat_messages():
    """List all chat messages"""
    return chat_messages_db

@router.get("/messages/{message_id}", response_model=ChatMessage)
def get_chat_message(message_id: int):
    """Get a specific chat message by ID"""
    for message in chat_messages_db:
        if message.id == message_id:
            return message
    raise HTTPException(status_code=404, detail="Chat message not found")

@router.post("/messages", response_model=ChatMessage)
def create_chat_message(message: ChatMessageCreate):
    """Create a new chat message"""
    new_id = max([m.id for m in chat_messages_db]) + 1 if chat_messages_db else 1
    new_message = ChatMessage(
        id=new_id,
        timestamp=datetime.now(),
        **message.dict()
    )
    chat_messages_db.append(new_message)
    return new_message

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessage])
def get_messages_for_session(session_id: int):
    """Get messages for a specific chat session"""
    return [message for message in chat_messages_db if message.session_id == session_id]

@router.put("/messages/{message_id}/read")
def mark_message_as_read(message_id: int):
    """Mark a message as read"""
    for index, message in enumerate(chat_messages_db):
        if message.id == message_id:
            chat_messages_db[index].is_read = True
            return {"message": "Message marked as read"}
    raise HTTPException(status_code=404, detail="Chat message not found")

# Chat Transcripts endpoints
@router.get("/transcripts", response_model=List[ChatTranscript])
def list_chat_transcripts():
    """List all chat transcripts"""
    return chat_transcripts_db

@router.get("/transcripts/{transcript_id}", response_model=ChatTranscript)
def get_chat_transcript(transcript_id: int):
    """Get a specific chat transcript by ID"""
    for transcript in chat_transcripts_db:
        if transcript.id == transcript_id:
            return transcript
    raise HTTPException(status_code=404, detail="Chat transcript not found")

@router.post("/transcripts", response_model=ChatTranscript)
def create_chat_transcript(transcript: ChatTranscriptCreate):
    """Create a new chat transcript"""
    new_id = max([t.id for t in chat_transcripts_db]) + 1 if chat_transcripts_db else 1
    new_transcript = ChatTranscript(
        id=new_id,
        created_at=datetime.now(),
        **transcript.dict()
    )
    chat_transcripts_db.append(new_transcript)
    return new_transcript

@router.get("/sessions/{session_id}/transcript", response_model=ChatTranscript)
def get_transcript_for_session(session_id: int):
    """Get transcript for a specific chat session"""
    for transcript in chat_transcripts_db:
        if transcript.session_id == session_id:
            return transcript
    raise HTTPException(status_code=404, detail="Chat transcript not found")

# Configuration endpoints
@router.get("/config/statuses", response_model=List[str])
def get_chat_status_options():
    """Get available chat status options"""
    return get_chat_statuses()

@router.get("/config/priorities", response_model=List[str])
def get_chat_priority_options():
    """Get available chat priority options"""
    return get_chat_priorities()