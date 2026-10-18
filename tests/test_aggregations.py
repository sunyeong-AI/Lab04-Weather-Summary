from weathersummary.aggregations import (
    PrecipitationAggregation,
    TemperatureAggregation,
)
from weathersummary.models import WeatherRecord


def test_precipitation_aggregation(sample_records: list[WeatherRecord]) -> None:
    """Test daily precipitation totals across multiple dates."""

    aggregation = PrecipitationAggregation()

    result = aggregation.calculate(sample_records)

    assert result["2026-10-08"] == 1.5
    assert result["2026-10-09"] == 2.0


def test_temperature_aggregation(sample_records: list[WeatherRecord]) -> None:
    """Test daily temperature statistics across multiple dates."""

    aggregation = TemperatureAggregation()

    result = aggregation.calculate(sample_records)

    assert result["2026-10-08"]["min"] == 15.0
    assert result["2026-10-08"]["max"] == 20.0
    assert result["2026-10-08"]["mean"] == 17.5

    assert result["2026-10-09"]["min"] == 10.0
    assert result["2026-10-09"]["max"] == 10.0
    assert result["2026-10-09"]["mean"] == 10.0


def test_temperature_aggregation_single_day() -> None:
    """Test minimum, maximum, and mean for one day."""

    records = [
        WeatherRecord("2026-10-08T10:00", 10, 1),
        WeatherRecord("2026-10-08T11:00", 20, 2),
        WeatherRecord("2026-10-08T12:00", 30, 3),
    ]

    result = TemperatureAggregation().calculate(records)

    assert result["2026-10-08"]["min"] == 10.0
    assert result["2026-10-08"]["max"] == 30.0
    assert result["2026-10-08"]["mean"] == 20.0


def test_precipitation_aggregation_single_day() -> None:
    """Test precipitation totals for multiple readings on one day."""

    records = [
        WeatherRecord("2026-10-08T10:00", 10, 1),
        WeatherRecord("2026-10-08T11:00", 20, 2),
        WeatherRecord("2026-10-08T12:00", 30, 3),
    ]

    result = PrecipitationAggregation().calculate(records)

    assert result["2026-10-08"] == 6.0
