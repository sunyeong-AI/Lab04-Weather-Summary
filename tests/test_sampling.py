import pytest

from weathersummary.models import WeatherRecord
from weathersummary.sampling import sample_days


def create_records() -> list[WeatherRecord]:
    """Create sample weather records for testing."""

    return [
        WeatherRecord(f"2026-10-{day:02d}T12:00", 15.0, 0.0) for day in range(10, 17)
    ]


def test_sample_days_are_reproducible() -> None:
    """The same seed should produce the same sampled dates."""

    records = create_records()

    first_result = sample_days(records, seed=42, sample_size=5)
    second_result = sample_days(records, seed=42, sample_size=5)

    assert first_result == second_result


@pytest.mark.parametrize("sample_size", [1, 3, 5])
def test_sample_days_returns_requested_number(sample_size: int) -> None:
    """Test sampling with different requested numbers of dates."""

    records = create_records()

    result = sample_days(records, seed=42, sample_size=sample_size)

    assert len(result) == sample_size


def test_sample_days_contains_unique_dates() -> None:
    """The sampled dates should not contain duplicates."""

    records = create_records()

    result = sample_days(records, seed=42, sample_size=5)

    assert len(result) == len(set(result))
