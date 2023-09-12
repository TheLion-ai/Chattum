"""Load bot sources as LangChain Documents + define custom tool SearchDocumentsTool."""

from app.app import database, file_storage
from app.routers.sources import remove_file
from bson import ObjectId
from fastapi import HTTPException
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
)
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.tools import Tool
from langchain.vectorstores import Chroma
from starlette.background import BackgroundTasks


def load_document(
    source_id: str, bot_id: str, background_tasks: BackgroundTasks
) -> Document:
    """Load bot source as a LangChain Document."""
    loaders = {
        "pdf": PyPDFLoader,
        "txt": UnstructuredFileLoader,
        "xls": UnstructuredExcelLoader,
    }

    source = database.sources.find_one_by_id(ObjectId(source_id))
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    file_path = file_storage.download_source(source_id, source.source_type, bot_id)

    extension = file_path.split(".")[-1]
    loader = loaders[extension](file_path)
    document = loader.load()

    background_tasks.add_task(remove_file, file_path)

    return document


class SearchDocumentsTool:
    """Custom tool using ChromaDB to search documents for the most relevant one."""

    def __init__(self, documents: list[Document]) -> None:
        """Initialize tool."""
        embedding_function = OpenAIEmbeddings()
        self.db = Chroma.from_documents(documents, embedding_function)

    def _run(self, query: str) -> Document:
        _docs = self.db.similarity_search(query)
        answer = _docs[0]
        return answer

    def _arun(self, query: str) -> None:
        raise NotImplementedError("This tool does not support async")

    def as_tool(self) -> Tool:
        """Return custom tool."""
        return Tool.from_function(
            func=self._run,
            name="Search Documents Tool",
            description="You must use this tool each time",
        )
