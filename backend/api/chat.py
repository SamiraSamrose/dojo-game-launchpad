# backend/api/chat.py
# Chat endpoints with encryption (Wootzapp)

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import ChatMessage
from backend.schemas import ChatRequest, ChatResponse
from backend.services.encryption import EncryptionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])
encryption_service = EncryptionService()


def get_db():
    """Database dependency - will be imported from main.py"""
    pass


@router.post("/send", response_model=ChatResponse)
async def send_chat_message(
    chat_request: ChatRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Send encrypted message to AI agent"""
    logger.info(f"Processing chat message from user: {user_id}")
    
    # Encrypt message if requested
    message = chat_request.message
    if chat_request.encrypted:
        encrypted_msg = encryption_service.encrypt_message(message)
        message = encrypted_msg
    
    # Get AI response
    ai_response = f"AI Agent: I'll help you with '{chat_request.message[:50]}...'"
    
    if chat_request.encrypted:
        encrypted_response = encryption_service.encrypt_message(ai_response)
        ai_response = encrypted_response
    
    # Save to database
    chat_msg = ChatMessage(
        user_id=user_id,
        message=message,
        response=ai_response,
        encrypted=chat_request.encrypted
    )
    db.add(chat_msg)
    db.commit()
    
    return ChatResponse(
        message="Message sent successfully",
        response=ai_response if not chat_request.encrypted else "Encrypted response",
        encrypted=chat_request.encrypted,
        encryption_provider="Wootzapp"
    )


@router.get("/history")
async def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    """Get user chat history"""
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).all()
    return {"messages": messages}


@router.delete("/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Delete a chat message"""
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    
    return {"message": "Message deleted successfully"}
