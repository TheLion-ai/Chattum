"""Create source endpoints."""

import logging
import os
from typing import Annotated, Optional, Union

import pydantic_models as pm
from app.app import chroma_controller, database, file_storage
from app.routes.bots import get_bot
from app.security import check_key
from bson import ObjectId
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from utils.scraping import scrape


def remove_file(path: str) -> None:
    """Remove tmp file form disk."""
    os.unlink(path)


router = APIRouter(prefix="/{username}/bots/{bot_id}/sources", tags=["sources"])


@router.get("", response_model=pm.SourceResponse)
def get_sources(bot_id: str, username: str, auth=Depends(check_key)) -> list[pm.Source]:
    """Get sources of bot by id."""
    bot = get_bot(bot_id, username)
    bot_sources = bot.sources
    # bot_sources = [str(source_id) for source_id in list(bot_sources)]
    sources = database.sources.find_by({"_id": {"$in": bot_sources}})

    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    source_ids = bot.sources

    sources = list(database.sources.find_by({"_id": {"$in": source_ids}}))

    return pm.SourceResponse(sources=sources)


@router.put("", response_model=pm.CreateSourceResponse)
def add_source(
    name: str,
    source_type: str,
    bot_id: str,
    username: str,
    file: Annotated[bytes, File()] = None,
    url: str = None,
    source_id: str = None,
    auth=Depends(check_key),
) -> pm.CreateSourceResponse:
    """Add source to bot by id."""
    if file is None and url is None:
        raise HTTPException(status_code=400, detail="No file or url provided")
    elif file is not None and url is not None:
        raise HTTPException(status_code=400, detail="Provide only file or url")

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
        # source.bot_id = ObjectId(bot_id)
        # source.username = username
        source.source_type = source_type

        database.sources.save(source)
    if source_id not in bot.sources:
        bot.sources.append(source_id)
        database.bots.save(bot)

    if file is not None:
        file_storage.upload_source(file, source_id, source_type, bot_id)
    if url is not None:
        try:
            file = scrape(url)
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail="Error scraping url")
        file_storage.upload_source(file, source_id, source_type, bot_id)

    chroma_controller.update_source(bot_id, source)
    return pm.CreateSourceResponse(
        message="Source added successfully!", source_id=str(source_id)
    )


@router.get("/{source_id}", response_model=pm.Source)
def get_source(
    bot_id: str, source_id: str, username: str, auth=Depends(check_key)
) -> pm.Source:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/{source_id}/file", response_model=pm.Source)
def get_source_file(
    bot_id: str,
    source_id: str,
    username: str,
    background_tasks: BackgroundTasks,
    auth=Depends(check_key),
) -> FileResponse:
    """Get source of bot by id."""
    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    file_path = file_storage.download_source(source_id, source.source_type, bot_id)
    background_tasks.add_task(remove_file, file_path)
    return FileResponse(file_path)


@router.delete("/{source_id}", response_model=pm.MessageResponse)
def delete_source(
    bot_id: str, source_id: str, username: str, auth=Depends(check_key)
) -> pm.MessageResponse:
    """Delete source of bot by id."""
    source = get_source(bot_id, source_id, username)

    bot = get_bot(bot_id, username)
    bot.sources.remove(ObjectId(source_id))
    database.bots.save(bot)

    database.sources.delete(source)
    file_storage.delete_source(source_id, source.source_type, bot_id)
    chroma_controller.delete_source(bot_id, source)
    return pm.MessageResponse(message="Source deleted successfully!")
