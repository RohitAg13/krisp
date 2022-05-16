import sys
from typing import Any

# # Installed # #
from loguru import logger

LoggerFormat = (
    "<green>{time:YY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "{function}: <level>{message}</level> | "
    "{extra} {exception}"
)

# Set custom logger
logger.remove()
logger.add(sys.stderr, level="DEBUG", format=LoggerFormat, enqueue=True)


def create_logger(name: str) -> Any:
    return logger
