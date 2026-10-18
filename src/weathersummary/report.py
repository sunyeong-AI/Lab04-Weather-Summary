import json
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .aggregations import PrecipitationAggregation, TemperatureAggregation
from .config import OUTPUT_PATH, SOURCE_URL, WeatherConfig
from .models import WeatherRecord
from .sampling import sample_days


def build_summary(
    records: list[WeatherRecord],
    source_url: str = SOURCE_URL,
    seed: int = 42,
    sample_size: int = 5,
) -> dict:
    """Build the final weather summary."""

    unique_dates = {record.date for record in records}

    summary = {
        "source_url": source_url,
        "record_count": len(records),
        "days_processed": len(unique_dates),
        "sample_days": sample_days(records, seed, sample_size),
    }

    aggregations = [
        ("daily_temperature", TemperatureAggregation()),
        ("daily_precipitation", PrecipitationAggregation()),
    ]

    for key, aggregation in aggregations:
        summary[key] = aggregation.calculate(records)

    return summary


def write_summary(
    summary: dict,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Write the summary to a JSON file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )


def write_run_info(
    config: WeatherConfig,
    output_path: Path,
) -> None:
    """Write configuration and software versions to a JSON file."""

    def get_version(package_name: str) -> str:
        """Return the installed version of a package."""

        try:
            return version(package_name)
        except PackageNotFoundError:
            return "not installed"

    run_info = {
        "settings": {
            "source_url": config.source_url,
            "timeout": config.timeout,
            "output_folder": str(config.output_folder),
            "seed": config.seed,
            "sample_size": config.sample_size,
            "log_level": config.log_level,
        },
        "python_version": platform.python_version(),
        "pytest_version": get_version("pytest"),
        "mypy_version": get_version("mypy"),
        "ruff_version": get_version("ruff"),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(run_info, indent=2),
        encoding="utf-8",
    )
