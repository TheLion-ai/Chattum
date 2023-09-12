"""Create source endpoints."""
import os
from typing import Annotated

import pydantic_models as pm
from app.app import database, file_storage
from app.routers.bots import get_bot
from bson import ObjectId
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks


def remove_file(path: str) -> None:
    """Remove tmp file form disk."""
    os.unlink(path)


router = APIRouter(prefix="/{username}/bots/{bot_id}/sources", tags=["sources"])


@router.get("", response_model=list[pm.Source])
def get_sources(bot_id: str, username: str) -> list[pm.Source]:
    """Get sources of bot by id."""
    bot = get_bot(bot_id, username)
    bot_sources = bot.sources
    # bot_sources = [str(source_id) for source_id in list(bot_sources)]
    sources = database.sources.find_by({"_id": {"$in": bot_sources}})

    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return list(sources)


@router.put("", response_model=pm.CreateSourceResponse)
def add_source(
    file: Annotated[bytes, File()],
    name: Annotated[str, Form()],
    source_type: Annotated[str, Form()],
    bot_id: str,
    username: str,
    source_id: Annotated[str, Form()] = None,
) -> pm.CreateSourceResponse:
    """Add source to bot by id."""
    bot = get_bot(bot_id, username)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")

    if source_id is None:
        source = pm.Source(
            name=name,
            bot_id=ObjectId(bot_id),
            username=username,
            source_type=source_type,
        )

        database.sources.save(source)
        source_id = source.id
    else:
        source = database.sources.find_one_by_id(ObjectId(source_id))
        if source is None:
            raise HTTPException(status_code=404, detail="Source not found")
        source.name = name
        source.bot_id = ObjectId(bot_id)
        source.username = username
        source.source_type = source_type

        database.sources.save(source)
    if source_id not in bot.sources:
        bot.sources.append(source_id)
        database.bots.save(bot)

    file_storage.upload_source(file, source_id, source_type, bot_id)
    return pm.CreateSourceResponse(
        message="Source added successfully!", source_id=str(source_id)
    )


@router.get("/{source_id}", response_model=pm.Source)
def get_source(bot_id: str, source_id: str, username: str) -> pm.Source:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/{source_id}/file", response_model=pm.Source)
def get_source_file(
    bot_id: str, source_id: str, username: str, background_tasks: BackgroundTasks
) -> FileResponse:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    file_path = file_storage.download_source(source_id, source.source_type, bot_id)
    background_tasks.add_task(remove_file, file_path)
    return FileResponse(file_path)


@router.delete("/{source_id}", response_model=pm.MessageResponse)
def delete_source(bot_id: str, source_id: str, username: str) -> pm.MessageResponse:
    """Delete source of bot by id."""
    source = get_source(bot_id, source_id, username)

    bot = get_bot(bot_id, username)
    bot.sources.remove(ObjectId(source_id))
    database.bots.save(bot)

    database.sources.delete(source)
    file_storage.delete_source(source_id, source.source_type, bot_id)
    return pm.MessageResponse(message="Source deleted successfully!")
