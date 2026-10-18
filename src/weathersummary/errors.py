class WeatherSummaryError(Exception):
    """Base exception for the WeatherSummary package."""


class SourceError(WeatherSummaryError):
    """Raised when weather data cannot be downloaded."""


class DataError(WeatherSummaryError):
    """Raised when weather data is missing or malformed."""


class SettingsError(WeatherSummaryError):
    """Raised when application settings are invalid."""
