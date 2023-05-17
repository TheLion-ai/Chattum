"""Module for managing basic bot operations."""
from database import bots_repository
from pydantic_models.bots import Bot


def create_bot(name: str, username: str) -> None:
    """Create a bot with the given name and username.

    Args:
        name (str): name of the bot
        username (str): username of the user associated with the bot
    """
    bot = Bot(name=name, username=username)
    bots_repository.save(bot)


def get_bots(username: str) -> list[Bot]:
    """Get all bots associated with the given username.

    Args:
        username (str): username of the user associated with the bot

    Returns:
        list[Bot]: list of bots associated with the given username
    """
    bots = bots_repository.find_by({"username": username})
    return list(bots)
