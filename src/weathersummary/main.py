import argparse
import logging
import sys
from pathlib import Path

from .config import load_config
from .errors import WeatherSummaryError
from .logging_config import setup_logging
from .report import build_summary, write_summary
from .sources import WeatherSource


logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Run the weather data aggregation program."""
    parser = argparse.ArgumentParser(description="Weather Summary")
    parser.add_argument(
        "--config",
        default="config/weathersummary.toml",
        help="Path to the TOML configuration file",
    )
    args = parser.parse_args(argv)

    try:
        config = load_config(Path(args.config))
        setup_logging(config.log_level)

        logger.info("Starting weather summary.")

        source = WeatherSource(config)
        records = source.fetch()

        logger.info("Fetched %d weather records.", len(records))

        summary = build_summary(records, config.source_url)

        output_path = config.output_folder / "summary.json"
        write_summary(summary, output_path)

        logger.info("Weather summary saved to %s", output_path)

        return 0

    except WeatherSummaryError as err:
        logger.error("Error: %s", err)
        return 1


if __name__ == "__main__":
    sys.exit(main())