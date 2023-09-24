"""Tools for searching documents for the most relevant one."""
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.tools import Tool
from langchain.vectorstores import Chroma


def search_documents_tool(db: Chroma, sources: list) -> Tool:
    """Search tool using ChromaDB to search documents for the most relevant one."""

    def _run(query: str) -> Document:
        _docs = db.similarity_search(query)
        answer = _docs[0]
        return answer

    def _arun(query: str) -> None:
        raise NotImplementedError("This tool does not support async")

    return Tool.from_function(
        func=_run,
        name="Search Documents Tool",
        description=f"Useful for searching information if you don't know the answer. Contains information about things such as {','.join([s.name for s in sources])} Input should be a search query.",
    )
