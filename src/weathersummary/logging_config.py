import logging
import sys


def setup_logging(log_level: str) -> None:
    """Configure logging using the specified log level."""

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )