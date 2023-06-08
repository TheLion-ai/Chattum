"""FastAPI application."""
from typing import Any

import bots
import pydantic_models as pm
from database import bots_repository
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from logger import init_logger
from bson import ObjectId

app = FastAPI()
init_logger(app)


@app.get("/health_check", response_model=pm.HealthCheckResponse)
def health_check() -> pm.HealthCheckResponse:
    """Health check endpoint."""
    return pm.HealthCheckResponse(status="ok")


@app.post("/")
def home() -> str:
    """Home endpoint."""
    hello_world = "Hello World!"
    return hello_world


@app.get("/bots", response_model=list[pm.Bot])
def bots_get(request: pm.BotsRequest) -> list[pm.Bot]:
    """Get all bots associated with the given username."""
    user_bots = bots.get_bots(request.username)

    return user_bots


@app.put("/bots", response_model=pm.CreateBotResponse)
def bots_put(bot: pm.Bot) -> pm.CreateBotResponse:
    """Create a bot with the given name and username."""
    bot = bots.create_bot(bot)
    return pm.CreateBotResponse(message="Bot created successfully!", bot_id=str(bot.id))


@app.get("/bots/{bot_id}")
def get_bot(bot_id: str) -> pm.Bot:
    """Get bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    return bot


@app.delete("/bots/{bot_id}")
def delete_bot(bot_id: str) -> pm.Bot:
    """Delete bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    bots_repository.delete(bot)
    return pm.MessageResponse(message="Bot deleted successfully!")


@app.get("/bots/{bot_id}/prompt", response_model=pm.PromptResponse)
def get_prompt(bot_id: str) -> str:
    """Get prompt of bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.PromptResponse(prompt=bot.prompt)


@app.put("/bots/{bot_id}/prompt", response_model=pm.MessageResponse)
def change_prompt(bot_id: str, request: pm.PromptRequest) -> pm.MessageResponse:
    """Change prompt of bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    bots.change_prompt(request.prompt, bot)
    return pm.MessageResponse(message="Prompt changed successfully!")


@app.put("/bots/{bot_id}/conversations", response_model=pm.CreateConversationResponse)
def put_conversations(bot_id: str, conversation: pm.Conversation) -> pm.CreateConversationResponse:
    """Create a conversation."""
    conversation.bot_id = ObjectId(bot_id)
    conversation = bots.create_conversation(conversation)
    return pm.CreateConversationResponse(
        message="Conversation created successfully!", conversation_id=str(conversation.id))


@app.get("/bots/{bot_id}/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> pm.Conversation:
    """Get conversation by id."""
    conversation = bots.get_conversation_by_id(conversation_id)
    return conversation


def custom_openapi() -> dict[str, Any]:
    """Customize the openapi schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Chattum",
        version="0.0.1",
        description="Chattum API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
