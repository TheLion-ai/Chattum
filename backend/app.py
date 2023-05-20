"""FastAPI application."""
from typing import Any

import bots
import pydantic_models as pm
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from logger import init_logger

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


@app.put("/bots", response_model=pm.MessageResponse)
def bots_put(bot: pm.Bot) -> pm.MessageResponse:
    """Create a bot with the given name and username."""
    bots.create_bot(bot)
    return pm.MessageResponse(message="Bot created successfully!")


@app.get("bots/{bot_id}", response_model=pm.Bot)
def get_bot(bot_id: str) -> pm.Bot:
    """Get bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    return bot


@app.get("bots/{bot_id}/prompt", response_model=str)
def get_prompt(bot_id: str) -> str:
    """Get prompt of bot by id."""
    bot = bots.get_bot_by_id(bot_id)

    return bot.prompt


@app.put("bots/{bot_id}/prompt", response_model=pm.MessageResponse)
def change_prompt(bot_id: str, prompt: str) -> pm.MessageResponse:
    """Change prompt of bot by id."""
    bot = bots.get_bot_by_id(bot_id)
    bots.change_prompt(prompt, bot)
    return pm.MessageResponse(message="Prompt changed successfully!")


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
