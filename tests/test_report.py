import json
from pathlib import Path

from weathersummary.config import load_config
from weathersummary.report import write_run_info


def test_write_run_info_with_tmp_path(tmp_path: Path) -> None:
    """Test that run information is saved as JSON in a temporary folder."""

    config = load_config(Path("config/weathersummary.toml"))
    output_path = tmp_path / "run_info.json"

    write_run_info(config, output_path)

    assert output_path.is_file()

    saved_data = json.loads(output_path.read_text(encoding="utf-8"))

    assert isinstance(saved_data, dict)
    assert saved_data
