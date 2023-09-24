# mypy: ignore-errors
"""create app instance."""
from contextlib import asynccontextmanager

from app.chroma import ChromaController
from app.database import Database, get_mongo_client
from app.file_storage import FileStorage, get_s3_client
from app.logger import init_logger
from fastapi import FastAPI

database = Database()
file_storage = FileStorage()
chroma_controller = ChromaController()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Startup event."""
    global database, file_storage, chroma_controller
    mongo_client = app.dependency_overrides.get(get_mongo_client, get_mongo_client)()
    database.init_repositories(mongo_client)

    minio_client = app.dependency_overrides.get(get_s3_client, get_s3_client)()
    file_storage.client = minio_client

    bots = database.bots.find_by({})
    chroma_controller.file_storage = file_storage
    for bot in bots:
        source_ids = bot.sources

        bot_sources = list(database.sources.find_by({"_id": {"$in": source_ids}}))
        chroma_controller.add_sources_to_bot(bot.id, bot_sources)

    yield
    database = None
    file_storage = None


app = FastAPI(lifespan=lifespan)
init_logger(app)
