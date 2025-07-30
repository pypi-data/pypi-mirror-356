"""Logging utilities for Shen."""

import logging

from rich.logging import RichHandler


def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration.

    Args:
        debug: Enable debug level logging
    """
    level = logging.DEBUG if debug else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=debug,
            )
        ],
    )

    # Set third-party loggers to WARNING
    for logger_name in ["urllib3", "httpx"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
