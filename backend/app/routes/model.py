"""Create model endpoints."""

from typing import Optional

import pydantic_models as pm
from app.app import database
from app.chat.models import available_models
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/model", tags=["models"])


@router.get("/available_models", response_model=list[pm.LLM])
def get_available_models() -> list[pm.LLM]:
    """Get available LLMs and their templates."""
    return [pm.LLM(**m.template) for m in available_models]


@router.get("", response_model=Optional[pm.LLM])
def get_model(bot_id: str) -> Optional[pm.LLM]:
    """Get model by username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    if bot is None:
        bot = database.workflows.find_one_by_id(ObjectId(bot_id))
    return bot.model


@router.put("", response_model=pm.MessageResponse)
def modify_model(bot_id: str, llm: pm.LLM) -> None:
    """Modify model by username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    if bot is None:
        workflow = database.workflows.find_one_by_id(ObjectId(bot_id))
        if workflow is None:
            return pm.MessageResponse(message="Bot or workflow not found!")
        workflow.model = llm
        database.workflows.save(workflow)
    else:
        bot.model = llm
        database.bots.save(bot)
    return pm.MessageResponse(message="Model updated successfully!")
