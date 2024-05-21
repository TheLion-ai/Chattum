"""Chattum API router."""
import copy
from typing import Any

import pydantic_models as pm
from app.app import app
from fastapi.openapi.utils import get_openapi

from .routes import (
    bots,
    chat,
    conversations,
    docs,
    model,
    prompts,
    sources,
    tools,
    workflows,
)

app.include_router(bots.router)
app.include_router(workflows.router)
app.include_router(prompts.router)
app.include_router(sources.router)
app.include_router(conversations.router)
app.include_router(chat.router)
app.include_router(docs.router)
app.include_router(tools.router)
app.include_router(model.router)


@app.get("/health_check", response_model=pm.HealthCheckResponse)
def health_check() -> pm.HealthCheckResponse:
    """Health check endpoint."""
    return pm.HealthCheckResponse(status="ok")


@app.post("/")
def home() -> str:
    """Home endpoint."""
    hello_world = "Hello World!"
    return hello_world


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
