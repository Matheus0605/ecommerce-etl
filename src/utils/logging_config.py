import logging
import os
from pythonjsonlogger import jsonlogger


def configure_logging(level: str | int = logging.INFO):
    """Configure root logger to output JSON-formatted logs.

    Keep function idempotent so modules can call it safely.
    """

    root = logging.getLogger()

    if root.handlers:
        # already configured
        return

    log_level = level
    if isinstance(level, str):
        log_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)

    root.setLevel(log_level)
    root.addHandler(handler)


# helper to read log level from env
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
configure_logging(LOG_LEVEL)
