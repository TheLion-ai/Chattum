"""FastAPI application."""
from typing import Any

import pydantic_models as pm
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from logger import init_logger

app = FastAPI()
init_logger(app)


@app.get("/health_check", response_model=pm.HealthCheckResponse)
async def health_check() -> pm.HealthCheckResponse:
    """Health check endpoint."""
    return pm.HealthCheckResponse(status="ok")


@app.post("/")
async def home() -> str:
    """Home endpoint."""
    hello_world = "Hello World!"
    return hello_world


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
