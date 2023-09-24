"""Create prompt endpoints."""
import pydantic_models as pm
from app.app import database
from app.routes.bots import get_bot
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/bots/{bot_id}/prompt", tags=["prompts"])


@router.get("", response_model=pm.PromptResponse)
def get_prompt(bot_id: str, username: str) -> str:
    """Get prompt of bot by id."""
    bot = get_bot(bot_id, username)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return pm.PromptResponse(prompt=bot.prompt)


@router.put("", response_model=pm.MessageResponse)
def change_prompt(
    bot_id: str,
    username: str,
    request: pm.PromptRequest,
) -> pm.MessageResponse:
    """Change prompt of bot by id."""
    bot = get_bot(bot_id, username)
    bot.prompt = request.prompt
    database.bots.save(bot)
    return pm.MessageResponse(message="Prompt changed successfully!")
