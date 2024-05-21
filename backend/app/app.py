# mypy: ignore-errors
"""create app instance."""
import logging
from contextlib import asynccontextmanager

from app.chroma import ChromaController
from app.database import Database, get_mongo_client
from app.file_storage import FileStorage, get_s3_client
from app.logger import init_logger
from fastapi import FastAPI, Request, Response

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


app = FastAPI(lifespan=lifespan, docs_url=None)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def api_logging(request: Request, call_next):
    request_body = await request.body()
    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    log_message = {
        "host": request.url.hostname,
        "endpoint": request.url.path,
        # "response": response_body.decode(errors="ignore"),
        "status_code": response.status_code,
        "method": request.method,
        "query_params": request.query_params,
        "headers": dict(request.headers),
        "request_body": request_body.decode(errors="ignore"),
    }
    logger.debug(log_message)
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
