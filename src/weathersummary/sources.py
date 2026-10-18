import requests

from .config import SOURCE_URL, TIMEOUT
from .models import WeatherRecord


class WeatherSource:
    """Fetch hourly weather records from the Open-Meteo API."""

    def __init__(self) -> None:
        self.url = SOURCE_URL
        self.timeout = TIMEOUT

    def fetch(self) -> list[WeatherRecord] | None:
        """Download weather data and create WeatherRecord objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

        except requests.RequestException:
            print("Could not download the weather data.")
            return None

        hourly_data = data["hourly"]
        times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        precipitations = hourly_data["precipitation"]

        records = []

        for time, temperature, precipitation in zip(
            times, temperatures, precipitations
        ):
            record = WeatherRecord(time, temperature, precipitation)
            records.append(record)

        return records
