"""Chattum API router."""
from typing import Any

import pydantic_models as pm
from app.app import app
from database import Database, get_database
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from logger import init_logger

from .routers import bots, prompts, sources

app.include_router(bots.router)
app.include_router(prompts.router)
app.include_router(sources.router)


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
