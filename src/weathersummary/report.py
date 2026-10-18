import json
from pathlib import Path

from .aggregations import PrecipitationAggregation, TemperatureAggregation
from .config import OUTPUT_PATH, SOURCE_URL
from .models import WeatherRecord


def build_summary(
    records: list[WeatherRecord],
    source_url: str = SOURCE_URL,
) -> dict:
    """Build the final weather summary."""

    unique_dates = {record.date for record in records}

    summary = {
        "source_url": source_url,
        "record_count": len(records),
        "days_processed": len(unique_dates),
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

    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")