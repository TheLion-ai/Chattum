"""FastAPI application."""
from typing import Any, List, Union

import pydantic_models as pm
from bson import ObjectId
from database import Database, get_database
from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/{username}/bots", response_model=list[pm.Bot])
def bots_get(username: str) -> list[pm.Bot]:
    """Get bots by username."""
    user_bots = list(database.bots.find_by({"username": username}))

    return user_bots


@app.put("/{username}/bots", response_model=pm.CreateBotResponse)
def bots_put(bot: pm.Bot, username: str) -> pm.CreateBotResponse:
    """Create a bot with the given name and username."""
    database.bots.save(bot)
    return pm.CreateBotResponse(message="Bot created successfully!", bot_id=str(bot.id))


@app.get("/{username}/bots/{bot_id}")
def get_bot(bot_id: str, username: str) -> Union[pm.Bot, None]:
    """Get bot by id."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@app.delete("/{username}/bots/{bot_id}")
def delete_bot(bot_id: str, username: str) -> pm.MessageResponse:
    """Delete bot by id."""
    bot = get_bot(bot_id, username)
    database.bots.delete(bot)
    return pm.MessageResponse(message="Bot deleted successfully!")


@app.get("/{username}/bots/{bot_id}/prompt", response_model=pm.PromptResponse)
def get_prompt(bot_id: str, username: str) -> str:
    """Get prompt of bot by id."""
    bot = get_bot(bot_id, username)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.PromptResponse(prompt=bot.prompt)


@app.put("/{username}/bots/{bot_id}/prompt", response_model=pm.MessageResponse)
def change_prompt(
    bot_id: str,
    username: str,
    request: pm.PromptRequest,
) -> pm.MessageResponse:
    """Change prompt of bot by id."""
    bot = get_bot(bot_id, username)
    bot.prompt = request.prompt
    database.bots.save(bot)
    return pm.MessageResponse(message="Prompt changed successfully!")


@app.get("/{username}/bots/{bot_id}/sources", response_model=pm.SourceResponse)
def get_sources(bot_id: str, username: str) -> List[pm.Source]:
    """Get sources of bot by id."""
    bot = get_bot(bot_id, username)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.SourceResponse(sources=bot.sources)


@app.put("/{username}/bots/{bot_id}/sources", response_model=pm.MessageResponse)
def add_source(source: pm.Source, username: str, bot_id: str) -> pm.MessageResponse:
    """Add source to bot by id."""
    database.sources.save(source)
    bot = get_bot(bot_id, username)
    bot.sources.append(source.id)
    database.bots.save(bot)
    return pm.MessageResponse(message="Source added successfully!")


@app.get("/{username}/bots/{bot_id}/sources/{source_id}", response_model=pm.Source)
def get_source(bot_id: str, source_id: str, username: str) -> pm.Source:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@app.delete(
    "/{username}/bots/{bot_id}/sources/{source_id}", response_model=pm.MessageResponse
)
def delete_source(bot_id: str, source_id: str, username: str) -> pm.MessageResponse:
    """Delete source of bot by id."""
    source = get_source(bot_id, source_id, username)
    database.sources.delete(source)
    return pm.MessageResponse(message="Source deleted successfully!")


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
