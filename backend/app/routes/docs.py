"""Routes for the docs."""

import copy
from typing import Optional

from app.app import app, database
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

router = APIRouter()


def add_example_to_param(
    spec: dict, param_name: str, example: Optional[str] = None
) -> None:
    """Add an example to a parameter in the OpenAPI spec."""
    if isinstance(spec, dict):
        for key, value in spec.items():
            # Check if the current dictionary is a "parameters" dictionary
            if key == "parameters":
                # Iterate through each parameter
                for param in value:
                    if param.get("name") == param_name:
                        # Add the example to the parameter
                        param["example"] = example
            # Recursively search in the value
            add_example_to_param(value, param_name, example)
    elif isinstance(spec, list):
        # If it's a list, iterate through it
        for item in spec:
            add_example_to_param(item, param_name, example)


@router.get("/custom_openapi/{username}", include_in_schema=False)
async def get_openapi_json(
    username: str, bot_id: Optional[str], workflow_id: Optional[str]
) -> dict:
    """Get the OpenAPI spec with examples filled in."""
    custom_openapi = copy.deepcopy(app.openapi())
    add_example_to_param(custom_openapi, "username", username)
    add_example_to_param(custom_openapi, "bot_id", bot_id)
    custom_openapi["info"]["title"] = "Chattum"
    custom_openapi["info"]["version"] = "0.0.1"
    custom_openapi["info"][
        "description"
    ] = f"Chattum API. Example are filled automatically with the username: {username} and bot_id: {bot_id}"

    # default keywords
    keywords = set(["default"])
    if bot_id != "None":
        bot_keywords = set(
            ["bots", "conversations", "model", "prompts", "sources", "chat", "tools"]
        )
        keywords = keywords.union(bot_keywords)
    if workflow_id != "None":
        workflow_keywords = set(["workflows", "model"])
        keywords = keywords.union(workflow_keywords)

    # remove paths that are not needed
    custom_openapi["paths"] = {
        path: data
        for path, data in custom_openapi["paths"].items()
        if any(
            keyword
            in data.get(method, {}).get("tags", ["default"])  # default has no tags
            for method in data.keys()
            for keyword in keywords
        )
    }
    return custom_openapi


@router.get("/docs/{username}", include_in_schema=False)
async def custom_swagger_ui_html(
    username: str, bot_id: Optional[str] = None, workflow_id: Optional[str] = None
) -> str:
    """Get the Swagger UI HTML with examples filled in."""
    query_params = ""
    if bot_id:
        query_params += f"?bot_id={bot_id}"
    if workflow_id:
        query_params += (
            f"&workflow_id={workflow_id}"
            if query_params
            else f"?workflow_id={workflow_id}"
        )
    return get_swagger_ui_html(
        openapi_url=f"/custom_openapi/{username}{query_params}",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
