from weathersummary.main import main


def test_main_invalid_config(capsys):
    """Test the exit code and error message for an invalid config file."""

    exit_code = main(["--config", "nonexistent_config.toml"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error:" in captured.err
