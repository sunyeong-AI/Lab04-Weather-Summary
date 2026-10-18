import logging


def setup_logging(log_level: str) -> None:
    """Configure logging using the specified log level."""

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(levelname)s: %(message)s",
        force=True,
    )