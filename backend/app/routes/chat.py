"""Create conversation endpoints."""

import pydantic_models as pm
from app.app import chroma_controller, database
from app.chat.chat_engine import ChatGPTEngine, GPTEngine, NewLangChainEngine
from app.chat.models import available_models_dict
from app.chat.tools import available_tools_dict
from app.chat.tools.document_search import SearchDocumentTool
from app.routes.bots import get_bot
from app.routes.conversations import (
    get_conversation,
    get_conversations,
    put_conversations,
)
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from langchain.tools import StructuredTool
from app.security import check_key
from fastapi import Depends

router = APIRouter(prefix="/{username}/bots/{bot_id}/chat", tags=["chat"])


def load_tools(bot_id: str) -> list[StructuredTool]:
    """Load tools for a bot."""
    loaded_tools = []
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    bot_tools = bot.tools
    bot_tools = list(database.tools.find_by({"_id": {"$in": bot_tools}}))
    for tool in bot_tools:
        loaded_tools.append(
            available_tools_dict[tool.name](
                tool.user_variables, tool.description_for_bot, tool.name_for_bot
            ).as_tool()
        )
    return loaded_tools


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
    if bot.model is None:
        raise HTTPException(
            status_code=404,
            detail="Bot model not found. Select a model in the bot settings.",
        )
    llm = available_models_dict[bot.model.name](bot.model.user_variables)

    bot_database = chroma_controller.get_database(bot_id)
    bot_tools = load_tools(bot_id)

    if bot_database is not None and bot_database["db"] is not None:
        bot_tools.append(
            SearchDocumentTool(bot_database["db"], bot_database["sources"]).as_tool()
        )

    if len(bot_tools) > 0 and llm.supports_tools:
        chat_engine = NewLangChainEngine(
            user_prompt=bot.prompt,
            messages=conversation.messages,
            tools=bot_tools,
            llm=llm.as_llm(),
        )
    else:
        # chat_engine = GripTapeEngine(
        #     user_prompt=bot.prompt, messages=conversation.messages, llm=llm.as_llm()
        # )
        if llm.model_type == "llm":
            chat_engine = GPTEngine(
                user_prompt=bot.prompt, messages=conversation.messages, llm=llm.as_llm()
            )
        elif llm.model_type == "chat":
            chat_engine = ChatGPTEngine(
                user_prompt=bot.prompt, messages=conversation.messages, llm=llm.as_llm()
            )

    response = chat_engine.chat(chat_input.message)
    conversation.messages = chat_engine.export_messages()

    put_conversations(bot.id, conversation)
    return pm.ChatResponse(message=response, conversation_id=conversation.id)
