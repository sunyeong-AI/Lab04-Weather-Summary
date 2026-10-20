
# WeatherSummary - Lab 04

WeatherSummary is a Python package that collects hourly weather data for Toronto from the Open-Meteo API. It calculates daily minimum, maximum, and mean temperatures and total daily precipitation.

Lab 04 improves the Lab 03 package by adding automated tests, custom exceptions, logging, type checking, TOML settings, and reproducible sampling.

## Setup

This project uses Python 3.11 and Conda.

Open a terminal in the project root folder and run:

```bash
conda env create -f environment.yml
conda activate weathersummary-lab04
pip install -r requirements.txt
pip install -e .
```

- `environment.yml` creates the Conda environment with Python 3.11 and pip using conda-forge.
- `requirements.txt` contains pinned package versions, including requests, pytest, mypy, ruff, and types-requests.
- `pip install -e .` installs the WeatherSummary package in editable mode.

The environment only needs to be created once. For later work, activate it with:

```bash
conda activate weathersummary-lab04
```

## Run

Run the program from the project root folder.

Use the default configuration:

```bash
python -m weathersummary.main
```

Or specify the configuration file:

```bash
python -m weathersummary.main --config config/weathersummary.toml
```

The program downloads hourly weather data and saves two JSON files in `data/processed/`:

- `summary.json`: weather summary and sampled dates.
- `run_info.json`: configuration settings and software versions.

The summary contains:

| Key | Description |
|---|---|
| `source_url` | URL used to download weather data. |
| `record_count` | Number of weather records processed. |
| `days_processed` | Number of unique dates. |
| `sample_days` | Dates selected using the random seed. |
| `daily_temperature` | Daily minimum, maximum, and mean temperatures. |
| `daily_precipitation` | Daily total precipitation. |


## Check it

Run the following commands to check the project:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

Each command checks a different part of the project:

- **Ruff format:** checks code formatting.
- **Ruff check:** checks import order, coding style, and possible errors.
- **mypy:** checks Python type hints.
- **pytest:** runs the automated tests.


## Settings

The program reads its configuration from `config/weathersummary.toml`.

| Setting | Current value | Description |
|---|---|---|
| `source_url` | Open-Meteo API URL for Toronto | Specifies the source of hourly weather data. |
| `timeout` | `10` | Maximum waiting time for an API request, in seconds. |
| `output_folder` | `data/processed` | Folder where the JSON output files are saved. |
| `seed` | `42` | Controls reproducible random sampling. |
| `sample_size` | `5` | Number of dates selected for sampling. |
| `log_level` | `INFO` | Controls logging levels. `INFO` hides DEBUG messages; `DEBUG` shows them. |


## Errors and exit codes

WeatherSummary uses custom exceptions to handle expected failures.

`WeatherSummaryError` is the base exception class. The other three classes inherit from it.

| Error class | When it is raised | What the user sees |
|---|---|---|
| `WeatherSummaryError` | Base class for expected package errors. Not raised directly. | No direct message; messages come from its subclasses. |
| `SettingsError` | The configuration file is missing or contains invalid settings. | `Error: Could not read the configuration file.` or `Error: Invalid log_level.` |
| `SourceError` | The API request fails because of a network or HTTP error. | `Error: Could not download the weather data.` |
| `DataError` | The API returns invalid JSON or data with an unexpected structure. |  `Error: The API returned invalid JSON data.` or `Error: The weather data has an invalid structure.` |

The package converts expected low-level errors into its own exceptions using `raise ... from err`. This preserves the original cause for debugging.

The `main()` function handles these expected errors, logs the failure, and prints a short message to standard error (`stderr`).

**Exit codes:**

- `0`: The program completed successfully.
- `1`: The program stopped because of an expected error, without a traceback.


## Reproducing a run

The seed and sample size are stored in `config/weathersummary.toml`:

```toml
seed = 42
sample_size = 5
```

The program uses `random.Random(seed)` to select dates for `sample_days`. Automated tests check that the same seed produces the same selection when the input is unchanged.

<sub><strong>Note:</strong> The <code>featured_shows</code> list in the assignment instructions was adapted to <code>sample_days</code> for this weather project. It selects dates instead of show names.</sub>

Each successful run creates `data/processed/run_info.json`, which records the source URL, timeout, output folder, seed, sample size, log level, Python version, and versions of pytest, mypy, and Ruff.

To reproduce a run:

1. Use the same project code and Git commit.
2. Create the environment using `environment.yml` and install the pinned packages from `requirements.txt`.
3. Use the same settings in `config/weathersummary.toml`.
4. Use the same input weather data, including the dates and their order.
5. Run the program using the command in the Run section.

**Important:** Open-Meteo data changes over time. The same seed produces the same `sample_days` only when the input dates and their order are unchanged. Reproducing an earlier run also requires the same settings, code, and software environment.

## What the tests cover

The project uses pytest to check important behavior without requiring an internet connection.

The tests cover:

- **WeatherRecord:** missing and invalid temperature and precipitation values.
- **TemperatureAggregation:** daily minimum, maximum, and mean temperatures.
- **PrecipitationAggregation:** daily precipitation totals.
- **Daily grouping:** correct calculations for one day and multiple days.
- **Data downloading:** network failures and invalid JSON responses.
- **Data parsing:** missing required fields.
- **Sampling:** sample size, unique dates, and reproducibility using the same seed.
- **Parametrized tests:** different sample sizes tested using `pytest.mark.parametrize`.
- **Exception testing:** expected errors and their messages using `pytest.raises(..., match=...)`.
- **Fixtures:** shared handmade weather records from `tests/conftest.py`.
- **Temporary files:** JSON writing tested with `tmp_path`.
- **Logging:** WARNING messages checked with `caplog`.
- **Main function:** successful execution, output file creation, failure exit code, and error messages.

The tests use handmade weather records and `monkeypatch` to replace actual API requests. They do not need an internet connection.

**What was not tested:**

The automated tests do not check whether the live Open-Meteo API is currently available. The API is an external service, and the assignment requires tests that work without a network connection.

The live API is checked separately by running the application.

## Known limitations

- **Changing weather data:** Open-Meteo provides updated data, so results may change between runs. Saving the original input data would help reproduce past results.

- **Missing and invalid values:** Missing or invalid values are skipped to avoid incorrect calculations. However, the summary does not show how many valid observations were used. Adding this count would make the results clearer.

- **Unequal data lengths:** The parser uses `zip()`, so extra values are ignored if the API lists have different lengths. Validating the list lengths would prevent unnoticed data loss.

- **Decimal precision:** Calculated values are saved without rounding and may contain long decimals. Formatting values for display would improve readability without changing the stored results.