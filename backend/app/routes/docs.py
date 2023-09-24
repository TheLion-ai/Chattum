"""Routes for the docs."""
import copy

from app.app import app
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

router = APIRouter()


def add_example_to_param(spec: dict, param_name: str, example: str) -> None:
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


@router.get("/custom_openapi/{username}/{bot_id}", include_in_schema=False)
async def get_openapi_json(username: str, bot_id: str) -> dict:
    """Get the OpenAPI spec with examples filled in."""
    custom_openapi = copy.deepcopy(app.openapi())
    add_example_to_param(custom_openapi, "username", username)
    add_example_to_param(custom_openapi, "bot_id", bot_id)
    custom_openapi["info"]["title"] = "Chattum"
    custom_openapi["info"]["version"] = "0.0.1"
    custom_openapi["info"][
        "description"
    ] = f"Chattum API. Example are filled automatically with the username: {username} and bot_id: {bot_id}"

    return custom_openapi


@router.get("/docs/{username}/{bot_id}", include_in_schema=False)
async def custom_swagger_ui_html(username: str, bot_id: str) -> str:
    """Get the Swagger UI HTML with examples filled in."""
    return get_swagger_ui_html(
        openapi_url=f"/custom_openapi/{username}/{bot_id}",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
