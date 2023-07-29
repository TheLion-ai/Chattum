"""Create conversation endpoints."""
from typing import Union

import pydantic_models as pm
from app.chat.chat_engine import ChatGPTEngine, ChatGPTEngine2
from app.routers.bots import get_bot
from app.routers.conversations import (
    get_conversation,
    get_conversations,
    put_conversations,
)
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/chat", tags=["chat"])


@router.post("", response_model=pm.ChatInput)
def chat(
    bot_id: str,
    username: str,
    chat_input: pm.ChatInput,
) -> pm.ChatResponse:
    """Get all conversations associated with the given bot."""
    bot = get_bot(bot_id, username)
    bot_conversations = get_conversations(bot_id)
    if any(
        conversation.id == chat_input.conversation_id
        for conversation in bot_conversations
    ):
        conversation = get_conversation(chat_input.conversation_id)

    else:
        conversation = pm.Conversation(bot_id=bot_id, messages=[])
    chat_engine = ChatGPTEngine2(user_prompt=bot.prompt, messages=conversation.messages)
    response = chat_engine.chat(chat_input.message)
    conversation.messages = chat_engine.export_messages()

    put_conversations(bot.id, conversation)
    return pm.ChatResponse(message=response, conversation_id=conversation.id)
