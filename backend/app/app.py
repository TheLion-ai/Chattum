# mypy: ignore-errors
"""create app instance."""
from contextlib import asynccontextmanager, contextmanager

from database import Database, get_mongo_client
from fastapi import FastAPI
from logger import init_logger

database = Database()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Startup event."""
    global database
    mongo_client = app.dependency_overrides.get(get_mongo_client, get_mongo_client)()
    database.init_repositories(mongo_client)
    yield
    database = None


app = FastAPI(lifespan=lifespan)
init_logger(app)
