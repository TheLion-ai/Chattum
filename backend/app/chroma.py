"""ChromaDB controller used for managing ChromaDB databases."""

import os
from typing import Optional

from app.file_storage import FileStorage
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
)
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic_models import Source


class ChromaController:
    """ChromaDB controller used for managing ChromaDB databases."""

    def __init__(self) -> None:
        """Initialize the ChromaDB controller."""
        self.file_storage: FileStorage = None
        self.db_path: str = "./chromadb"
        self.databases: dict = {}
        self.embedding_function = OpenAIEmbeddings()

        self.loaders = {
            "pdf": PyPDFLoader,
            "txt": UnstructuredFileLoader,
            "xls": UnstructuredExcelLoader,
            "url": UnstructuredFileLoader,
        }

    def add_sources_to_bot(self, bot_id: str, sources: list) -> None:
        """Add sources to the ChromaDB client."""
        bot_db_path = os.path.join(self.db_path, str(bot_id))
        if os.path.exists(bot_db_path):
            print(f"Found existing database for bot {bot_id}")
            bot_db = Chroma(
                persist_directory=bot_db_path,
                embedding_function=self.embedding_function,
            )
        else:
            documents = self.__load_sources_as_documents(sources, bot_id)
            bot_db = self.__init_bot_database(bot_id, sources, documents, bot_db_path)
        self.databases[str(bot_id)] = {"db": bot_db, "sources": sources}

    def __load_sources_as_documents(self, sources: list, bot_id: str) -> list[Document]:
        """Load bot source as a LangChain Document."""
        documents = []

        for source in sources:
            file_path = self.file_storage.download_source(
                source.id, source.source_type, bot_id
            )
            extension = file_path.split(".")[-1]
            loader = self.loaders[extension](file_path)
            document = loader.load()
            documents.extend(document)
            os.remove(file_path)

        return documents

    def __init_bot_database(
        self, bot_id: str, sources: list, documents: list[Document], bot_db_path: str
    ) -> Chroma:
        """Create a ChromaDB database from a list of documents."""
        print(f"Creating chroma database for bot {bot_id}")
        if len(documents) == 0 or len(sources) == 0:
            return None
        ids = [str(source.id) for source in sources]
        bot_db = Chroma.from_documents(
            documents,
            self.embedding_function,
            ids=ids,
            persist_directory=bot_db_path,
        )
        return bot_db

    def get_database(self, bot_id: str) -> dict:
        """Get chroma database for bot."""
        return self.databases.get(str(bot_id), None)

    def update_source(self, bot_id: str, source: Source) -> None:
        """Update a source in the ChromaDB client."""
        print(f"Updating source {source.id} for bot {bot_id}")

        file_path = self.file_storage.download_source(
            source.id, source.source_type, bot_id
        )

        extension = file_path.split(".")[-1]
        loader = self.loaders[extension](file_path)
        document = loader.load()[0]

        text = document.page_content
        metadata = document.metadata
        if self.embedding_function is None:
            raise ValueError(
                "For update, you must specify an embedding function on creation."
            )
        embeddings = self.embedding_function.embed_documents([text])

        bot_db = self.get_database(bot_id) or {"db": None, "sources": []}
        if bot_db["db"] is None:
            bot_db["db"] = Chroma(
                persist_directory=os.path.join(self.db_path, str(bot_id)),
                embedding_function=self.embedding_function,
            )
            bot_db["sources"] = []

        bot_db["db"]._collection.add(  # type: ignore
            ids=[str(source.id)],
            embeddings=embeddings,
            documents=[text],
            metadatas=[metadata],
        )

        for source in bot_db["sources"]:
            if source.id == source.id:
                source = source
        else:
            bot_db["sources"].append(source)
        self.databases[str(bot_id)] = bot_db

        os.remove(file_path)

    def delete_source(self, bot_id: str, source_id: set) -> None:
        """Delete a source from the ChromaDB client."""
        bot_db = self.get_database(bot_id)
        bot_db["db"].delete(ids=[str(source_id)])
        bot_db["sources"] = [
            source for source in bot_db["sources"] if source.id != source_id
        ]
        self.databases[str(bot_id)] = bot_db
