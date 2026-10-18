import json

from .config import SOURCE_URL, OUTPUT_PATH
from .aggregations import TemperatureAggregation, PrecipitationAggregation


def build_summary(records):
    """Build the final weather summary."""

    unique_dates = {record.date for record in records}

    summary = {
        "source_url": SOURCE_URL,
        "record_count": len(records),
        "days_processed": len(unique_dates)
    }

    aggregations = [
        ("daily_temperature", TemperatureAggregation()),
        ("daily_precipitation", PrecipitationAggregation())
    ]

    for key, aggregation in aggregations:
        summary[key] = aggregation.calculate(records)

    return summary


def write_summary(summary):
    """Write the summary to a JSON file."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )