"""Module for managing basic bot operations."""
from bson import ObjectId
from database import bots_repository
from pydantic_models.bots import Bot


def create_bot(bot: Bot) -> Bot:
    """
    Create a bot with the given name and username.

    Args:
    ----
        bot (Bot): bot to be created
    """
    bots_repository.save(bot)
    bot = bots_repository.find_one_by_id(bot.id)
    return bot


# trunk-ignore(ruff/D417)
def get_bots(username: str) -> list[Bot]:
    """Get all bots associated with the given username.

    Args:
    ----
        username (str): username of the user associated with the bot

    Returns:
    -------
        list[Bot]: list of bots associated with the given username
    """
    bots = list(bots_repository.find_by({"username": username}))
    return bots


def get_bot_by_id(bot_id: str) -> Bot:
    """
    Get bot by id.

    Args:
    ----
        bot_id (str): bot id

    Returns:
    -------
        Bot: bot with the given id
    """
    bot = bots_repository.find_one_by_id(ObjectId(bot_id))
    return bot
