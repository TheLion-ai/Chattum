"""Prompt management functions."""
from database import bots_repository
from pydantic_models.bots import Bot


def change_prompt(prompt: str, bot: Bot) -> Bot:
    """
    Change the prompt of the bot.

    Args:
    ----
        prompt (str): new prompt
        bot (Bot): bot to change prompt of

    Returns:
    -------
        Bot: bot with the new prompt
    """
    bot.prompt = prompt
    bots_repository.save(bot)
