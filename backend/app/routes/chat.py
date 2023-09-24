"""Create conversation endpoints."""

import pydantic_models as pm
from app.app import chroma_controller
from app.chat.chat_engine import ChatGPTEngine, ReactEngine
from app.chat.tools.document_search import search_documents_tool
from app.routes.bots import get_bot
from app.routes.conversations import (
    get_conversation,
    get_conversations,
    put_conversations,
)
from fastapi import APIRouter

router = APIRouter(prefix="/{username}/bots/{bot_id}/chat", tags=["chat"])


@router.post("", response_model=pm.ChatInput)
def chat(
    bot_id: str,
    username: str,
    chat_input: pm.ChatInput,
) -> pm.ChatResponse:
    """Chat with a bot. If the conversation id is not provided, a new conversation is created."""
    bot = get_bot(bot_id, username)
    bot_conversations = get_conversations(bot_id)
    # documents = [str(source.id) for source in bot_sources]

    if any(
        conversation.id == chat_input.conversation_id
        for conversation in bot_conversations
    ):
        conversation = get_conversation(chat_input.conversation_id)

    else:
        conversation = pm.Conversation(bot_id=bot_id, messages=[])

    bot_database = chroma_controller.get_database(bot_id)
    if bot_database is not None and bot_database["db"] is not None:
        tools = [search_documents_tool(bot_database["db"], bot_database["sources"])]
        chat_engine = ReactEngine(
            user_prompt=bot.prompt,
            messages=conversation.messages,
            tools=tools,
        )
    else:
        tools = []
        chat_engine = ChatGPTEngine(
            user_prompt=bot.prompt,
            messages=conversation.messages,
        )

    response = chat_engine.chat(chat_input.message)
    conversation.messages = chat_engine.export_messages()

    put_conversations(bot.id, conversation)
    return pm.ChatResponse(message=response, conversation_id=conversation.id)
