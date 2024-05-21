"""Tests for tools."""

import json

import requests

tools_templates = {
    "Post Tool": {
        "User Variables": {
            "url": "",
            "body": """{
                    "username" : "{{username}}",
                    "favorite_color" : "{{favorite_color}}"
                }
                """,
        },
        "Prompt": "Your role is to collect names and favorite colors from the user and sent it to the server",
        "Message": "Hello, my name is John and my favorite color is blue",
    },
}


def common_tool_test(test_client, tool_name, tool_template, api_key):
    """
    Test function for a common tool.

    This function tests the following:
    - Adding a tool to a bot
    - Checking if the tool was added successfully
    - Setting user variables for the tool
    - Setting a prompt for the bot
    - Starting a conversation with the bot
    - Checking if the conversation was successful

    Args:
        test_client (TestClient): The test client to use for making requests
        tool_name (str): The name of the tool to test
        tool_template (dict): A dictionary containing the tool template to use for testing
    """
    tool = available_tools_dict[tool_name]
    for user_variable in tool["user_variables"]:
        user_variable["value"] = tool_template["User Variables"][user_variable["name"]]
    test_client.put(
        f"/{username}/bots/{bot_id}/tools", json=tool, headers={"X-API-Key": api_key}
    )

    bot_tools = test_client.get(
        f"/{username}/bots/{bot_id}/tools", headers={"X-API-Key": api_key}
    ).json()
    assert bot_tools[0]["name"] == tool_name
    for user_variable in bot_tools[0]["user_variables"]:
        assert (
            user_variable["value"]
            == tool_template["User Variables"][user_variable["name"]]
        )

    test_client.put(
        f"/{username}/bots/{bot_id}/prompt",
        json={"prompt": tool_template["Prompt"]},
        headers={"X-API-Key": api_key},
    )

    response = test_client.post(
        f"/{username}/bots/{bot_id}/chat",
        json={"message": tool_template["Message"]},
        headers={"X-API-Key": api_key},
    )
    conversation_id = response.json()["conversation_id"]

    response = test_client.get(
        f"/{username}/bots/{bot_id}/conversations/{conversation_id}",
        headers={"X-API-Key": api_key},
    )
    assert response.status_code == 200


def delete_all_tools(test_client, api_key):
    """Delete all tools."""
    bot_tools = test_client.get(
        f"/{username}/bots/{bot_id}/tools", headers={"X-API-Key": api_key}
    ).json()
    for tool in bot_tools:
        test_client.delete(
            f"/{username}/bots/{bot_id}/tools/{tool['id']}",
            headers={"X-API-Key": api_key},
        )

    bot_tools = test_client.get(
        f"/{username}/bots/{bot_id}/tools", headers={"X-API-Key": api_key}
    ).json()
    assert bot_tools == []


def test_create_bot(test_client, model_template, api_key) -> None:
    """Creates bot for testing."""
    global username
    global bot_id
    username = "test_user"
    bot_id = test_client.put(
        f"/{username}/bots", json=model_template, headers={"X-API-Key": api_key}
    ).json()["bot_id"]


def test_get_available_tools(test_client, api_key):
    """Test the get available tools endpoint."""
    global available_tools_dict
    available_tools = test_client.get(
        f"/{username}/bots/{bot_id}/tools/available_tools",
        headers={"X-API-Key": api_key},
    )
    assert available_tools.status_code == 200
    available_tools_dict = {tool["name"]: tool for tool in available_tools.json()}


def test_post_tool(test_client, api_key):
    """Test the post tool."""

    token_id = requests.post("https://webhook.site/token").json()["uuid"]
    url = "https://webhook.site/" + token_id

    tool_template = tools_templates["Post Tool"]
    tool_template["User Variables"]["url"] = url
    common_tool_test(test_client, "Post Tool", tools_templates["Post Tool"], api_key)

    # Check if the request was sent to the server
    r = requests.get(
        "https://webhook.site/token/" + token_id + "/requests?sorting=newest"
    )
    assert json.loads(r.json()["data"][0]["content"]) == {
        "username": "John",
        "favorite_color": "blue",
    }

    delete_all_tools(test_client, api_key)
