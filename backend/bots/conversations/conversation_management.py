"""Conversation management functions."""
from bson import ObjectId
from database import conversations_repository
from pydantic_models.conversations import Conversation


def create_conversation(conversation: Conversation) -> Conversation:
    conversations_repository.save(conversation)
    conversation = conversations_repository.find_one_by_id(conversation.id)
    return conversation


def get_conversation_by_id(conversation_id: str) -> Conversation:
    conversation = conversations_repository.find_one_by_id(ObjectId(conversation_id))
    return conversation
