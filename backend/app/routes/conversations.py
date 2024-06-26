"""Create conversation endpoints."""

from datetime import datetime
from typing import Union

import pydantic_models as pm
from app.app import database
from app.routes.bots import get_bot
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.security import check_key
from fastapi import Depends

router = APIRouter(
    prefix="/{username}/bots/{bot_id}/conversations", tags=["conversations"]
)


@router.get("", response_model=list[pm.Conversation])
def get_conversations(bot_id: str, auth=Depends(check_key)) -> list[pm.Conversation]:
    """Get all conversations associated with the given bot."""
    bot_conversations = list(
        database.conversations.find_by({"bot_id": ObjectId(bot_id)})
    )
    return bot_conversations


@router.put("", response_model=pm.CreateConversationResponse)
def put_conversations(
    bot_id: str, conversation: pm.Conversation, auth=Depends(check_key)
) -> pm.CreateConversationResponse:
    """Create a conversation."""
    conversation.bot_id = ObjectId(bot_id)
    conversation.last_message_time = datetime.now()
    database.conversations.save(conversation)
    conversation = database.conversations.find_one_by_id(conversation.id)
    return pm.CreateConversationResponse(
        message="Conversation created successfully!",
        conversation_id=str(conversation.id),
    )


@router.get("/{conversation_id}")
def get_conversation(conversation_id: str, auth=Depends(check_key)) -> pm.Conversation:
    """Get conversation by id."""
    conversation = database.conversations.find_one_by_id(ObjectId(conversation_id))
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str, auth=Depends(check_key)
) -> pm.MessageResponse:
    """Delete conversation by id."""
    conversation = get_conversation(conversation_id)
    database.conversations.delete(conversation)
    return pm.MessageResponse(message="Conversation deleted successfully!")
