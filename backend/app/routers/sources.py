"""Create source endpoints."""
from typing import Union

import pydantic_models as pm
from app.app import database
from app.routers.bots import get_bot
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/sources", tags=["sources"])


@router.get("", response_model=pm.SourceResponse)
def get_sources(bot_id: str, username: str) -> list[str]:
    """Get sources of bot by id."""
    bot = get_bot(bot_id, username)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.SourceResponse(sources=bot.sources)


@router.put("", response_model=pm.CreateSourceResponse)
def add_source(
    source: pm.Source, username: str, bot_id: str
) -> pm.CreateSourceResponse:
    """Add source to bot by id."""
    database.sources.save(source)
    bot = get_bot(bot_id, username)
    bot.sources.append(source.id)
    database.bots.save(bot)
    return pm.CreateSourceResponse(
        message="Source added successfully!", source_id=str(source.id)
    )


@router.get("/{source_id}", response_model=pm.Source)
def get_source(bot_id: str, source_id: str, username: str) -> pm.Source:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.delete("/{source_id}", response_model=pm.MessageResponse)
def delete_source(bot_id: str, source_id: str, username: str) -> pm.MessageResponse:
    """Delete source of bot by id."""
    source = get_source(bot_id, source_id, username)
    database.sources.delete(source)
    return pm.MessageResponse(message="Source deleted successfully!")
