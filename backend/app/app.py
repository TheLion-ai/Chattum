# mypy: ignore-errors
"""create app instance."""
from contextlib import asynccontextmanager

from app.database import Database, get_mongo_client
from app.file_storage import FileStorage, get_s3_client
from app.logger import init_logger
from fastapi import FastAPI

database = Database()
file_storage = FileStorage()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Startup event."""
    global database, file_storage
    mongo_client = app.dependency_overrides.get(get_mongo_client, get_mongo_client)()
    database.init_repositories(mongo_client)

    minio_client = app.dependency_overrides.get(get_s3_client, get_s3_client)()
    file_storage.client = minio_client
    yield
    database = None
    file_storage = None


app = FastAPI(lifespan=lifespan)
init_logger(app)
