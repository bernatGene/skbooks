import logging

from rich.logging import RichHandler

from settings import settings


def setup_logging():
    """
    Set up logging for the application based on settings.
    """
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True,  # To override any existing basicConfig
    )

    for module, level in settings.LOG_LEVELS.items():
        logging.getLogger(module).setLevel(level.upper())
