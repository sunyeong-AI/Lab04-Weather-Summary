import random

from .models import WeatherRecord


def sample_days(
    records: list[WeatherRecord],
    seed: int,
    sample_size: int,
) -> list[str]:
    """Select unique dates reproducibly using a random seed."""

    unique_dates = sorted({record.date for record in records})

    rng = random.Random(seed)

    selected_days = rng.sample(
        unique_dates,
        min(sample_size, len(unique_dates)),
    )

    return selected_days
