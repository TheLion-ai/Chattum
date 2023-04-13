import logging
import sys

import json_logging


def init_logger(app):
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
