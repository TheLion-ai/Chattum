"""Create bot endpoints."""

from typing import Union

import pydantic_models as pm
from app.app import database
from app.chat.tools import available_tools
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/tools", tags=["tools"])


@router.get("/available_tools", response_model=list[pm.Tool])
def get_available_tools(username: str) -> list[pm.Tool]:
    return [pm.Tool(**t.template) for t in available_tools]


@router.put("/", response_model=pm.MessageResponse)
def put_tool(tool: pm.Tool, username: str, bot_id: str) -> pm.MessageResponse:
    # TODO: update existing tool
    """Create a tool with the given name and username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    database.tools.save(tool)

    bot.tools.append(tool.id)
    database.bots.save(bot)
    return pm.MessageResponse(message="Tool updated successfully!")


@router.get("/", response_model=list[pm.Tool])
def get_tools(username: str, bot_id: str) -> list[pm.Tool]:
    """Get tools by username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    bot_tools = bot.tools
    tools = list(database.tools.find_by({"_id": {"$in": bot_tools}}))

    return tools


@router.delete("/{tool_id}", response_model=pm.MessageResponse)
def delete_tool(tool_id: str, username: str, bot_id: str) -> pm.MessageResponse:
    """Delete tool by id."""
    tool = database.tools.find_one_by_id(ObjectId(tool_id))
    bot = database.bots.find_one_by_id(ObjectId(bot_id))

    database.tools.delete(tool)
    bot.sources.remove(ObjectId(tool_id))

    return pm.MessageResponse(message="Tool deleted successfully!")
