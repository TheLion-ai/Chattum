"""Create model endpoints."""

import pydantic_models as pm
from app.app import database
from app.chat.models import available_models
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/model", tags=["tools"])


@router.get("/available_models", response_model=list[pm.Model])
def get_available_models() -> list[pm.Model]:
    """Get available LLMs and their templates."""
    return [pm.Model(**m.template) for m in available_models]


@router.get("/", response_model=pm.Model)
def get_model(bot_id: str) -> pm.Model:
    """Get model by username."""
    bot = database.bots.find_one_by_id(ObjectId(bot_id))
    return bot.model


@router.put("/", response_model=pm.MessageResponse)
def modify_model() -> None:
    """TODO."""
    pass  # TODO
