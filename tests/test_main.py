import json
from pathlib import Path

import pytest

from weathersummary.main import main
from weathersummary.models import WeatherRecord
from weathersummary.sources import WeatherSource


def test_main_invalid_config(capsys):
    """Test the exit code and error message for an invalid config file."""

    exit_code = main(["--config", "nonexistent_config.toml"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.err.splitlines() == [
    "Error: Could not read the configuration file."
]


def test_main_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a successful run without accessing the internet."""

    # 1. Create temporary folders and a configuration file.
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    config_path = tmp_path / "test_config.toml"

    config_path.write_text(
        "\n".join(
            [
                'source_url = "https://example.com/weather"',
                "timeout = 10",
                f'output_folder = "{output_folder.as_posix()}"',
                "seed = 42",
                "sample_size = 2",
                'log_level = "INFO"',
            ]
        ),
        encoding="utf-8",
    )

    # 2. Replace the actual API request with sample data.
    def fake_fetch(self: WeatherSource) -> list[WeatherRecord]:
        return [
            WeatherRecord("2026-10-08T10:00", 15.0, 0.0),
            WeatherRecord("2026-10-08T11:00", 20.0, 1.5),
            WeatherRecord("2026-10-09T10:00", 10.0, 2.0),
        ]

    monkeypatch.setattr(WeatherSource, "fetch", fake_fetch)

    # 3. Run the program.
    exit_code = main(["--config", str(config_path)])

    # 4. Verify successful execution and output files.
    assert exit_code == 0

    summary_path = output_folder / "summary.json"
    run_info_path = output_folder / "run_info.json"

    assert summary_path.is_file()
    assert run_info_path.is_file()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    run_info = json.loads(run_info_path.read_text(encoding="utf-8"))

    assert isinstance(summary, dict)
    assert isinstance(run_info, dict)
