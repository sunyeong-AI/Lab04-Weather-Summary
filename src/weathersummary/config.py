import tomllib
from dataclasses import dataclass
from pathlib import Path

from .errors import SettingsError

SOURCE_URL = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto"

TIMEOUT = 10

OUTPUT_PATH = Path("data/processed/summary.json")


@dataclass(frozen=True)
class WeatherConfig:
    """Store weather summary settings."""

    source_url: str
    timeout: int
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str


def load_config(path: Path = Path("config/weathersummary.toml")) -> WeatherConfig:
    """Load and validate settings from a TOML file."""
    try:
        with path.open("rb") as file:
            data = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as err:
        raise SettingsError("Could not read the configuration file.") from err

    try:
        source_url = data["source_url"]
        timeout = data["timeout"]
        output_folder = data["output_folder"]
        seed = data["seed"]
        sample_size = data["sample_size"]
        log_level = data["log_level"]
    except KeyError as err:
        raise SettingsError(f"Missing configuration setting: {err}") from err

    if not isinstance(source_url, str) or not source_url.startswith("https://"):
        raise SettingsError("source_url must be an HTTPS URL.")

    if type(timeout) is not int or timeout <= 0:
        raise SettingsError("timeout must be a positive integer.")

    if not isinstance(output_folder, str) or not output_folder.strip():
        raise SettingsError("output_folder must be a non-empty string.")

    if type(seed) is not int:
        raise SettingsError("seed must be an integer.")

    if type(sample_size) is not int or sample_size <= 0:
        raise SettingsError("sample_size must be a positive integer.")

    if not isinstance(log_level, str) or log_level.upper() not in (
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ):
        raise SettingsError("Invalid log_level.")

    return WeatherConfig(
        source_url=source_url,
        timeout=timeout,
        output_folder=Path(output_folder),
        seed=seed,
        sample_size=sample_size,
        log_level=log_level.upper(),
    )
