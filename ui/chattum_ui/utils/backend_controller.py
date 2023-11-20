"""Functions exchanging information from frontend with backend."""
from typing import Annotated

import requests
from settings import BACKEND_URL, USERNAME


def get_bots() -> list[dict]:
    """Get a list of available bots.

    Returns:
        list[dict]: a list of created bots.
    """
    bots = requests.get(f"{BACKEND_URL}/{USERNAME}/bots").json()

    return bots


def create_new_bot(bot_name: str) -> None:
    """Create a new bot with a given name.

    Args:
        bot_name (str): a name for a new bot
    """
    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots",
        json={"name": bot_name, "username": USERNAME},
    )
    assert response.status_code == 200


def get_sources(bot_id: str) -> list[dict]:
    """Get a list of available source for the selected bot.

    Returns:
        list[dict]: a list of created sources for the bot.
    """
    sources = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources").json()[
        "sources"
    ]

    return sources


def get_source(bot_id: str, source_id: str) -> dict:
    """Get a source with a given id.

    Args:
        bot_id (str): id of the bot to which the source belongs
        source_id (str): id of the source to get
    Returns:
        dict: a source with a given id.
    """
    source = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources/{source_id}")
    return source.json()


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
    ).json()
    return file


def delete_source(bot_id: str, source_id: str) -> None:
    """Delete a source with a given id.

    Args:
        bot_id (str): id of the bot to which the source belongs
        source_id (str): id of the source to delete
    """
    response = requests.delete(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources/{source_id}",
    )
    assert response.status_code == 200


def create_new_source(
    source_name: str, source_type: str, bot_id: str, file: bytes = None, url: str = None
) -> None:
    """Create a new source for the bot with a given name.

    Args:
        source_name (str): a name for a new source for the bot
    """
    if source_type == "url":
        response = requests.put(
            f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources",
            params={
                "name": source_name,
                "source_type": source_type,
                "url": url,
            },
        )
    else:
        response = requests.put(
            f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/sources",
            params={
                "name": source_name,
                "source_type": source_type,
            },
            files={"file": file},  # type: ignore
        )
    print(response.status_code)
    print(response.text)


def create_new_prompt(prompt: str, bot_id: str) -> None:
    """Create a new prompt based on text from text area."""
    response = requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/prompt", json={"prompt": prompt}
    )


def get_prompt(bot_id: str) -> str:
    """Get the current prompt of a bot.

    Returns:
        str: bot's prompt.
    """
    prompt = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/prompt").json()[
        "prompt"
    ]

    return prompt


def get_conversations(bot_id: str) -> list[dict]:
    """Get a list of conversations involving given bot."""
    conversations = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/conversations"
    ).json()
    return conversations


def get_conversation(bot_id: str, conversation_id: str) -> dict | None:  # type: ignore
    """Get a conversation by id."""
    response = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/conversations/{conversation_id}"
    )
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"error: {response.status_code} {response.text}")


def get_bot(bot_id: str) -> dict:
    """Get a bot by id."""
    bot = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}").json()
    return bot


def send_message(bot_id: str, conversation_id: str, message: str) -> tuple[str, str]:
    """Send a message to a bot and get a response."""

    body = (
        {"message": message, "conversation_id": str(conversation_id)}
        if conversation_id is not None
        else {"message": message}
    )

    response = requests.post(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/chat",
        json=body,
    ).json()
    return response["message"], response["conversation_id"]


def get_available_tools(bot_id: str) -> list[dict]:
    """Get a list of available tools for the selected bot.

    Returns:
        list[dict]: a list of created tools for the bot.
    """
    tools = requests.get(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools/available_tools"
    ).json()

    return tools


def create_new_tool(bot_id: str, tool_name: str, user_variables: list) -> None:
    """Create a new tool for the bot with a given name and user variabes."""
    # TODO: update existing tool
    requests.put(
        f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools",
        json={
            "name": tool_name,
            "description": "test",
            "user_variables": user_variables,
        },
    )


def get_tools(bot_id: str) -> list[dict]:
    """Get a list of available tools for the selected bot.

    Returns:
        list[dict]: a list of created tools for the bot.
    """
    tools = requests.get(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools").json()

    return tools


def delete_tool(bot_id: str, tool_id: str) -> None:
    """Delete a tool with a given id."""
    requests.delete(f"{BACKEND_URL}/{USERNAME}/bots/{bot_id}/tools/{tool_id}")
