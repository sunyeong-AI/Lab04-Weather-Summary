import argparse
import logging
import sys
from pathlib import Path

from .config import load_config
from .errors import WeatherSummaryError
from .logging_config import setup_logging
from .report import build_summary, write_run_info, write_summary
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

    setup_logging("INFO")

    try:
        config = load_config(Path(args.config))
        logging.getLogger().setLevel(config.log_level.upper())

        logger.info("Starting weather summary.")

        source = WeatherSource(config)
        records = source.fetch()

        logger.info("Fetched %d weather records.", len(records))

        summary = build_summary(
            records,
            source_url=config.source_url,
            seed=config.seed,
            sample_size=config.sample_size,
        )

        output_path = config.output_folder / "summary.json"
        write_summary(summary, output_path)

        run_info_path = config.output_folder / "run_info.json"
        write_run_info(config, run_info_path)

        logger.info("Weather summary saved to %s", output_path)
        logger.info("Run information saved to %s", run_info_path)

        return 0

    except WeatherSummaryError as err:
        logger.error("Error: %s", err)
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
