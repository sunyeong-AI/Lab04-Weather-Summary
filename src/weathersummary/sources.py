import requests

from .config import SOURCE_URL, TIMEOUT, WeatherConfig
from .errors import DataError, SourceError
from .models import WeatherRecord


def download_weather_data(url: str, timeout: int) -> dict:
    """Download weather data from the API."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        raise SourceError("Could not download the weather data.") from err
    except ValueError as err:
        raise DataError("The API returned invalid JSON data.") from err


def parse_weather_data(data: dict) -> list[WeatherRecord]:
    """Convert API data into WeatherRecord objects."""
    try:
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

    except (KeyError, TypeError) as err:
        raise DataError("The weather data has an invalid structure.") from err


class WeatherSource:
    """Fetch hourly weather records from the Open-Meteo API."""

    def __init__(self, config: WeatherConfig | None = None) -> None:
        if config is None:
            self.url = SOURCE_URL
            self.timeout = TIMEOUT
        else:
            self.url = config.source_url
            self.timeout = config.timeout

    def fetch(self) -> list[WeatherRecord]:
        """Download and parse weather data."""
        data = download_weather_data(self.url, self.timeout)

        return parse_weather_data(data)