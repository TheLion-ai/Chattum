"""Functions exchanging information from frontend with backend."""

import time
from typing import Annotated, Callable, Optional

import requests
import streamlit as st
from constants import BACKEND_URL, USERNAME
from langchain.memory import ChatMessageHistory


def endpoint(
    success_message: str = None, error_message: str = None, progress_message: str = ""
) -> Callable:
    def inner_decorator(f: Callable) -> Callable:
        def wrapped(*args: list, **kwargs: dict) -> dict | list | None:
            try:
                response = f(*args, **kwargs)
                if not response.status_code == 200:
                    raise Exception(response.json())
                if success_message:
                    st.toast(success_message, icon="✅")
                return response.json()
            except Exception as e:
                print(e)
                error_message = "Error"  # noqa: F823
                if "response" in locals():
                    error_message += f": {response.json()}"
                st.toast(error_message, icon="❌")
                return None

        return wrapped

    return inner_decorator


@endpoint(error_message="Error getting bots")
def get_bots() -> requests.Response:
    """Get a list of available bots.

    Returns:
        list[dict]: a list of created bots.
    """
    return requests.get(f"{BACKEND_URL}/{USERNAME}/bots")


@endpoint(error_message="Error getting workflows")
def get_workflows() -> requests.Response:
    """Get a list of available workflows.

    Returns:
        list[dict]: a list of created workflows.
    """
    return requests.get(f"{BACKEND_URL}/{USERNAME}/workflows")


@endpoint(success_message="Bot created", error_message="Error creating bot")
def create_new_bot(bot_name: str) -> requests.Response:
    """Create a new bot with a given name.

    Args:
        bot_name (str): a name for a new bot
    """
    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots",
        json={"name": bot_name, "username": USERNAME},
    )
    return response


@endpoint(success_message="Workflow created", error_message="Error creating workflow")
def create_new_workflow(workflow: dict) -> requests.Response:
    """Create a new workflow with a given name and task."""
    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/workflows",
        json=workflow | {"username": USERNAME},
    )
    return response


@endpoint()
def get_sources(bot_id: str) -> requests.Response:
    """Get a list of available source for the selected bot.

    Returns:
        list[dict]: a list of created sources for the bot.
    """
    return requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources")


@endpoint()
def get_source(bot_id: str, source_id: str) -> requests.Response:
    """Get a source with a given id.

    Args:
        bot_id (str): id of the bot to which the source belongs
        source_id (str): id of the source to get
    Returns:
        dict: a source with a given id.
    """
    source = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources/{source_id}")
    return source


def get_source_file(bot_id: str, source_id: str) -> bytes:
    """Get a source file with a given id.

    Args:
        bot_id (str): id of the bot to which the source belongs
        source_id (str): id of the source to get
    Returns:
        bytes: a source file with a given id.
    """
    file = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources/{source_id}/file"
    ).content
    return file


@endpoint(success_message="Source deleted", error_message="Error deleting source")
def delete_source(bot_id: str, source_id: str) -> requests.Response:
    """Delete a source with a given id.

    Args:
        bot_id (str): id of the bot to which the source belongs
        source_id (str): id of the source to delete
    """
    response = requests.delete(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources/{source_id}",
    )
    return response


@endpoint(success_message="Source updated", error_message="Error updating source")
def create_new_source(
    source_name: str,
    source_type: str,
    bot_id: str,
    file: bytes = None,
    url: str = None,
    source_id: str = None,
) -> requests.Response:
    """Create a new source for the bot with a given name.

    Args:
        source_name (str): a name for a new source for the bot
    """
    # st.write(file)
    if source_type == "url":
        response = requests.put(
            f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources",
            params={
                "name": source_name,
                "source_type": source_type,
                "url": url,
                "source_id": source_id,
            },
        )
    else:
        response = requests.put(
            f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources",
            params={
                "name": source_name,
                "source_type": source_type,
                "source_id": source_id,
            },
            files={"file": file},  # type: ignore
        )
    return response


@endpoint(success_message="Prompt updated", error_message="Error updating prompt")
def create_new_prompt(prompt: str, bot_id: str) -> requests.Response:
    """Create a new prompt based on text from text area."""
    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/prompt",
        json={"prompt": prompt},
    )
    return response


@endpoint(error_message="Error getting prompt")
def get_prompt(bot_id: str) -> requests.Response:
    """Get the current prompt of a bot.

    Returns:
        str: bot's prompt.
    """
    prompt = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/prompt")

    return prompt


@endpoint(error_message="Error getting conversations")
def get_conversations(bot_id: str) -> requests.Response:
    """Get a list of conversations involving given bot."""
    conversations = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/conversations"
    )
    return conversations


@endpoint(error_message="Error getting conversation")
def get_conversation(bot_id: str, conversation_id: str) -> requests.Response:  # type: ignore
    """Get a conversation by id."""
    response = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/conversations/{conversation_id}"
    )
    return response


@endpoint(error_message="Error getting bot")
def get_bot(bot_id: str) -> requests.Response:
    """Get a bot by id."""
    return requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}")


@endpoint(error_message="Error getting workflow")
def get_workflow(workflow_id: str) -> requests.Response:
    """Get a workflow by id."""
    return requests.get(f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}")


@endpoint(error_message="Error in conversation")
def send_message(bot_id: str, conversation_id: str, message: str) -> requests.Response:
    """Send a message to a bot and get a response."""
    return requests.post(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/chat",
        json={"message": message, "conversation_id": str(conversation_id)},
    )


@endpoint(error_message="Error in prediction")
def run_prediction(workflow_id: str, message: str) -> requests.Response:
    """Run a prediction for a given message."""
    return requests.post(
        f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}/run",
        json={"username": USERNAME, "message": message},
    )


@endpoint(error_message="Error loading available tools")
def get_available_tools(bot_id: str) -> requests.Response:
    """Get a list of available tools for the selected bot.

    Returns:
        list[dict]: a list of created tools for the bot.
    """
    tools = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools/available_tools"
    )
    return tools


@endpoint(success_message="Tool updated", error_message="Error updating tool")
def create_or_edit_tool(
    bot_id: str,
    tool_name: str,
    bot_description: str,
    user_variables: list,
    tool_id: Optional[str] = None,
    name_for_bot: Optional[str] = None,
) -> requests.Response:
    """Create a new tool for the bot with a given name and user variabes."""

    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools",
        json={
            "id": tool_id,
            "name": tool_name,
            "description_for_bot": bot_description,
            "user_variables": user_variables,
            "name_for_bot": name_for_bot,
        },
    )
    return response


@endpoint(error_message="Error getting tools")
def get_tools(bot_id: str) -> requests.Response:
    """Get a list of available tools for the selected bot.

    Returns:
        list[dict]: a list of created tools for the bot.
    """
    return requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools")


@endpoint(success_message="Tool deleted", error_message="Error deleting tool")
def delete_tool(bot_id: str, tool_id: str) -> requests.Response:
    """Delete a tool with a given id."""
    return requests.delete(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools/{tool_id}")


@endpoint(error_message="Error getting model")
def get_model(bot_id: str) -> requests.Response:
    """Get the current model of the bot or workflow."""
    return requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/model")


@endpoint(error_message="Error getting available models")
def get_available_models(bot_id: str) -> requests.Response:
    """Get a list of available models.

    Returns:
        list[dict]: a list of available models.
    """
    return requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/model/available_models"
    )


@endpoint(error_message="Error changing model")
def change_model(bot_id: str, model: dict) -> requests.Response:
    """Change the current model of the bot."""
    return requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/model",
        json=model,
    )


@endpoint(error_message="Error changing model")
def change_workflow_model(workflow_id: str, model: dict) -> requests.Response:
    """Change the current model of the workflow."""
    return requests.put(
        f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}/model",
        json=model,
    )


@endpoint(error_message="Error calibrating model", success_message="Model calibrated")
def calibrate_workflow_model(workflow_id: str, x: list, y: list) -> requests.Response:
    """Calibrate the model of the workflow."""
    return requests.post(
        f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}/calibrate",
        json={"x": x, "y": y},
    )


@endpoint(
    error_message="Evaluating workflow", success_message="Model evaluation finished"
)
def evaluate_workflow(workflow_id: str, x: list, y: list) -> requests.Response:
    """Calibrate the model of the workflow."""
    return requests.post(
        f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}/evaluate",
        json={"x": x, "y": y},
    )


@endpoint(error_message="Error changing instructions")
def change_instructions(
    workflow_id: str, instructions: str, classes: list[str]
) -> requests.Response:
    """Change the instructions and classes of the workflow."""
    return requests.put(
        f"{BACKEND_URL}/{USERNAME}/workflows/{workflow_id}/instructions",
        json={"instructions": instructions, "classes": classes},
    )


@endpoint(error_message="Error editing workflow", success_message="Workflow changed")
def create_or_edit_workflow(workflow: dict) -> requests.Response:
    return requests.put(
        f"{BACKEND_URL}/{USERNAME}/workflows",
        json=workflow,
    )
