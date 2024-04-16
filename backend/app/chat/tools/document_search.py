"""Tools for searching documents for the most relevant one."""

from langchain.schema import Document
from langchain.tools import Tool
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel, Field

from .base_tool import ToolTemplate


class SearchDocumentTool(ToolTemplate):
    """Tool for searching documents for the most relevant one."""

    name: str = "Search Documents Tool"
    description: str = "Search for the most relevant document based on the query"

    name_for_bot: str = "search_documents"

    user_variables: list = []

    @property
    def args_schema(self) -> BaseModel:
        """Return the args schema for langchain."""

        class ArgsSchema(BaseModel):
            query: str = Field(description="The query to search for")

        return ArgsSchema

    def __init__(self, db: Chroma, sources: list) -> None:
        """Initialize the tool."""
        self.db = db
        self.sources = sources

    @property
    def description_for_bot(self) -> str:  # type: ignore
        """Return the tool description for llm."""
        return f"Useful for searching information if you don't know the answer. Contains information about things such as {','.join([s.name for s in self.sources])}"

    def run(self, *args: list, **kwargs: dict) -> str:
        """Run the tool by sending a post request to the url with the body."""
        query = kwargs.get("query", None) or args[0]
        _docs = self.db.similarity_search(query)
        answer = _docs[0].page_content
        return answer
