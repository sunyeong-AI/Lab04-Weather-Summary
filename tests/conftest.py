import pytest

from weathersummary.models import WeatherRecord


@pytest.fixture
def sample_records():
    """Provide sample weather records for aggregation tests."""
    return [
        WeatherRecord("2026-10-08T10:00", 15.0, 0.0),
        WeatherRecord("2026-10-08T11:00", 20.0, 1.5),
        WeatherRecord("2026-10-09T10:00", 10.0, 2.0),
    ]
