import pytest
import requests

from weathersummary.errors import DataError, SourceError
from weathersummary.sources import download_weather_data, parse_weather_data


def test_download_weather_data_network_error(monkeypatch):
    """Test that a network failure raises SourceError."""

    def fake_get(url, timeout):
        raise requests.ConnectionError("Network connection failed")

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(SourceError):
        download_weather_data("https://example.com", 10)


def test_download_weather_data_invalid_json(monkeypatch):
    """Test that invalid JSON raises DataError."""

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(DataError):
        download_weather_data("https://example.com", 10)


def test_parse_weather_data_missing_field():
    """Test that missing weather data raises DataError."""

    data = {
        "hourly": {
            "time": ["2026-10-01T10:00"],
            "temperature_2m": [15.0],
            # precipitation is missing
        }
    }

    with pytest.raises(DataError):
        parse_weather_data(data)