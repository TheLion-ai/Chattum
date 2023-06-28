"""create app instance."""
from database import Database, get_database
from fastapi import FastAPI
from logger import init_logger

app = FastAPI()
init_logger(app)

database: Database = None

# @app.on_event("startup")
# async def startup_event() -> None:
#     """Startup event."""
#     global database
database = app.dependency_overrides.get(get_database, get_database)()
