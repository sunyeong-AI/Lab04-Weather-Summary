import unittest

from weathersummary.aggregations import (
    PrecipitationAggregation,
    TemperatureAggregation,
)
from weathersummary.models import WeatherRecord


class TestWeatherSummary(unittest.TestCase):
    """Test weather record cleaning."""

    def test_invalid_values(self):
        """Check that invalid weather values become None."""

        record = WeatherRecord("2026-10-08T10:00", "abc", -2)

        self.assertIsNone(record.temperature)
        self.assertIsNone(record.precipitation)

    def test_missing_values(self):
        """Check that missing weather values remain None."""

        record = WeatherRecord("2026-10-08T10:00", None, None)

        self.assertIsNone(record.temperature)
        self.assertIsNone(record.precipitation)


def test_precipitation_aggregation(sample_records):
    """Test daily precipitation totals using sample records."""
    aggregation = PrecipitationAggregation()

    result = aggregation.calculate(sample_records)

    assert result["2026-10-08"] == 1.5
    assert result["2026-10-09"] == 2.0


def test_temperature_aggregation(sample_records):
    """Test daily temperature statistics using sample records."""
    aggregation = TemperatureAggregation()

    result = aggregation.calculate(sample_records)

    assert result["2026-10-08"]["min"] == 15.0
    assert result["2026-10-08"]["max"] == 20.0
    assert result["2026-10-08"]["mean"] == 17.5

    assert result["2026-10-09"]["min"] == 10.0
    assert result["2026-10-09"]["max"] == 10.0
    assert result["2026-10-09"]["mean"] == 10.0


if __name__ == "__main__":
    unittest.main()
