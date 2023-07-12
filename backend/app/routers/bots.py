"""Create bot endpoints."""

from typing import Union

import pydantic_models as pm
from app.app import database
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots", tags=["bots"])


@router.get("/", response_model=list[pm.Bot])
def bots_get(username: str) -> list[pm.Bot]:
    """Get bots by username."""
    user_bots = list(database.bots.find_by({"username": username}))

    return user_bots


@router.put("/", response_model=pm.CreateBotResponse)
def bots_put(bot: pm.Bot, username: str) -> pm.CreateBotResponse:
    """Create a bot with the given name and username."""
    database.bots.save(bot)
    return pm.CreateBotResponse(message="Bot created successfully!", bot_id=str(bot.id))


@router.get("/{bot_id}")
def get_bot(bot_id: str, username: str) -> Union[pm.Bot, None]:
    """Get bot by id."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.delete("/{bot_id}")
def delete_bot(bot_id: str, username: str) -> pm.MessageResponse:
    """Delete bot by id."""
    bot = get_bot(bot_id, username)
    database.bots.delete(bot)
    # Delete all conversations involving the bot
    conversations = list(database.conversations.find_by({"bot_id": ObjectId(bot_id)}))
    for conversation in conversations:
        database.conversations.delete(conversation)
    return pm.MessageResponse(message="Bot deleted successfully!")
