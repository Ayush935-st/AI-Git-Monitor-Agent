"""
Centralized logging configuration.

This module provides a singleton logger that can be used across the
entire AI Git Monitoring application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerManager:
    """
    Creates and manages the application's logger.

    Features
    --------
    - Console logging
    - Rotating log files
    - Consistent formatting
    - Singleton logger
    """

    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:

        if cls._logger:
            return cls._logger

        # ---------------------------------------------------
        # Create logs directory
        # ---------------------------------------------------

        log_directory = Path("logs")
        log_directory.mkdir(exist_ok=True)

        log_file = log_directory / "application.log"

        # ---------------------------------------------------
        # Logger
        # ---------------------------------------------------

        logger = logging.getLogger("AIGitMonitoringAgent")
        logger.setLevel(logging.INFO)

        if logger.hasHandlers():
            logger.handlers.clear()

        # ---------------------------------------------------
        # Formatter
        # ---------------------------------------------------

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # ---------------------------------------------------
        # Console Handler
        # ---------------------------------------------------

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # ---------------------------------------------------
        # File Handler
        # ---------------------------------------------------

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # ---------------------------------------------------
        # Register Handlers
        # ---------------------------------------------------

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.propagate = False

        cls._logger = logger

        return logger


logger = LoggerManager.get_logger()