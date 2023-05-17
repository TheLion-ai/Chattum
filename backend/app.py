"""FastAPI application."""
from typing import Any

import pydantic_models as pm
from bots import create_bot, get_bots
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
    bots = get_bots(request.username)
    return bots


@app.put("/bots", response_model=pm.MessageResponse)
def bots_put(bot: pm.Bot) -> pm.MessageResponse:
    """Create a bot with the given name and username."""
    create_bot(bot)
    return pm.MessageResponse(message="Bot created successfully!")


def custom_openapi() -> dict[str, Any]:
    """Customize the openapi schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Chatttum",
        version="0.0.1",
        description="Chatttum API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
