"""Json logger for FastAPI."""
import logging
import sys

import fastapi
import json_logging


def init_logger(app: fastapi.FastAPI) -> None:
    """Initialize the logger."""
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
