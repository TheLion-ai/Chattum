"""FastAPI application."""
from typing import Any, Union

import pydantic_models as pm
from bson import ObjectId
from database import Database, get_database
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from logger import init_logger

app = FastAPI()
init_logger(app)

database: Database = None


@app.on_event("startup")
def startup_event() -> None:
    """Startup event."""
    global database
    database = app.dependency_overrides.get(get_database, get_database)()


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
    """Get bots by username."""
    user_bots = list(database.bots.find_by({"username": request.username}))

    return user_bots


@app.put("/bots", response_model=pm.CreateBotResponse)
def bots_put(bot: pm.Bot) -> pm.CreateBotResponse:
    """Create a bot with the given name and username."""
    database.bots.save(bot)
    return pm.CreateBotResponse(message="Bot created successfully!", bot_id=str(bot.id))


@app.get("/bots/{bot_id}")
def get_bot(bot_id: str) -> Union[pm.Bot, None]:
    """Get bot by id."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    return bot


@app.delete("/bots/{bot_id}")
def delete_bot(bot_id: str) -> pm.MessageResponse:
    """Delete bot by id."""
    bot = get_bot(bot_id)
    database.bots.delete(bot)
    # Delete all conversations involving the bot
    conversations = get_conversations(bot_id)
    for conversation in conversations:
        database.conversations.delete(conversation)
    return pm.MessageResponse(message="Bot deleted successfully!")


@app.get("/bots/{bot_id}/prompt", response_model=pm.PromptResponse)
def get_prompt(bot_id: str) -> str:
    """Get prompt of bot by id."""
    bot = get_bot(bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.PromptResponse(prompt=bot.prompt)


@app.put("/bots/{bot_id}/prompt", response_model=pm.MessageResponse)
def change_prompt(bot_id: str, request: pm.PromptRequest) -> pm.MessageResponse:
    """Change prompt of bot by id."""
    bot = get_bot(bot_id)
    bot.prompt = request.prompt
    database.bots.save(bot)
    return pm.MessageResponse(message="Prompt changed successfully!")


@app.get("/bots/{bot_id}/conversations", response_model=list[pm.Conversation])
def get_conversations(bot_id: str) -> list[pm.Conversation]:
    """Get all conversations associated with the given bot."""
    bot_conversations = list(
        database.conversations.find_by({"bot_id": ObjectId(bot_id)})
    )
    return bot_conversations


@app.put("/bots/{bot_id}/conversations", response_model=pm.CreateConversationResponse)
def put_conversations(
    bot_id: str, conversation: pm.Conversation
) -> pm.CreateConversationResponse:
    """Create a conversation."""
    conversation.bot_id = ObjectId(bot_id)
    database.conversations.save(conversation)
    conversation = database.conversations.find_one_by_id(conversation.id)
    return pm.CreateConversationResponse(
        message="Conversation created successfully!",
        conversation_id=str(conversation.id),
    )


@app.get("/bots/{bot_id}/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> pm.Conversation:
    """Get conversation by id."""
    conversation = database.conversations.find_one_by_id(ObjectId(conversation_id))
    return conversation


@app.delete("/bots/{bot_id}/conversations/{conversation_id}")
def delete_conversation(conversation_id: str) -> pm.MessageResponse:
    """Delete conversation by id."""
    conversation = get_conversation(conversation_id)
    database.conversations.delete(conversation)
    return pm.MessageResponse(message="Conversation deleted successfully!")


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
