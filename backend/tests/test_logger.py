from backend.utils.logger import logger

logger.info("Logger initialized successfully.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")

try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("An exception occurred during testing.")