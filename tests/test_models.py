import unittest

from weathersummary.aggregations import PrecipitationAggregation, TemperatureAggregation
from weathersummary.models import WeatherRecord


class TestWeatherSummary(unittest.TestCase):
    """Test weather record cleaning and daily aggregations."""

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

    def test_temperature_aggregation(self):
        """Check daily minimum, maximum, and mean temperatures."""

        records = [
            WeatherRecord("2026-10-08T10:00", 10, 1),
            WeatherRecord("2026-10-08T11:00", 20, 2),
            WeatherRecord("2026-10-08T12:00", 30, 3),
        ]

        result = TemperatureAggregation().calculate(records)

        self.assertEqual(result["2026-10-08"]["min"], 10.0)
        self.assertEqual(result["2026-10-08"]["max"], 30.0)
        self.assertEqual(result["2026-10-08"]["mean"], 20.0)

    def test_precipitation_aggregation(self):
        """Check daily precipitation totals."""

        records = [
            WeatherRecord("2026-10-08T10:00", 10, 1),
            WeatherRecord("2026-10-08T11:00", 20, 2),
            WeatherRecord("2026-10-08T12:00", 30, 3),
        ]

        result = PrecipitationAggregation().calculate(records)

        self.assertEqual(result["2026-10-08"], 6.0)


if __name__ == "__main__":
    unittest.main()