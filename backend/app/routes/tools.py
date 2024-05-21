"""Create bot endpoints."""

from typing import Union

import pydantic_models as pm
from app.app import database
from app.chat.tools import available_tools
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.security import check_key
from fastapi import Depends

router = APIRouter(prefix="/{username}/bots/{bot_id}/tools", tags=["tools"])


@router.get("/available_tools", response_model=list[pm.Tool])
def get_available_tools(username: str, auth=Depends(check_key)) -> list[pm.Tool]:
    """Get available tools and their templates."""
    print([t.template for t in available_tools])
    return [pm.Tool(**t.template) for t in available_tools]


@router.put("", response_model=pm.MessageResponse)
def put_tool(
    new_tool: pm.Tool, username: str, bot_id: str, auth=Depends(check_key)
) -> pm.MessageResponse:
    """Create a tool with the given name and username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    if new_tool.id is None:
        database.tools.save(new_tool)
        bot.tools.append(new_tool.id)
        database.bots.save(bot)
    else:
        tool = database.tools.find_one_by_id(ObjectId(new_tool.id))
        if tool is None:
            raise HTTPException(status_code=404, detail="Tool not found")
        tool.name_for_bot = new_tool.name_for_bot
        tool.description_for_bot = new_tool.description_for_bot
        tool.user_variables = new_tool.user_variables
        database.tools.save(tool)
    return pm.MessageResponse(message="Tool updated successfully!")


@router.get("", response_model=list[pm.Tool])
def get_tools(username: str, bot_id: str, auth=Depends(check_key)) -> list[pm.Tool]:
    """Get tools by username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    bot_tools = bot.tools
    tools = list(database.tools.find_by({"_id": {"$in": bot_tools}}))

    return tools


@router.delete("/{tool_id}", response_model=pm.MessageResponse)
def delete_tool(
    tool_id: str, username: str, bot_id: str, auth=Depends(check_key)
) -> pm.MessageResponse:
    """Delete tool by id."""
    tool = database.tools.find_one_by_id(ObjectId(tool_id))
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    database.tools.delete(tool)
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    bot.tools.remove(ObjectId(tool_id))
    database.bots.save(bot)

    return pm.MessageResponse(message="Tool deleted successfully!")
