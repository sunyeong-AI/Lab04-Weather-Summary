# Weather Summary

This Python package retrieves hourly weather data for Toronto from the Open-Meteo API and summarizes daily temperature and precipitation. It calculates daily minimum, maximum, and mean temperatures, along with total daily precipitation.

## Data source

URL: https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto

One record: One hour of weather data, including time, temperature, and precipitation.

Number of records: Approximately 168 hourly records over seven days.

## Setup

Create the Conda environment with Python 3.11:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate weathersummary
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install the package:

```bash
pip install -e .
```

## Run

```bash
python main.py
```

**Note:** The program saves the weather summary to `data/processed/summary.json`.

## Test

```bash
python -m unittest discover -s tests
```

## Layout

- `models.py`: Contains the WeatherRecord class. It stores individual weather records and handles invalid values, so other modules can focus on their own tasks.
- `sources.py`: Contains the WeatherSource class. It gets weather data from the API, so data collection is separate from calculations.
- `aggregations.py`: Contains the Aggregation class and its subclasses. It calculates weather statistics, so calculations are kept in one module.
- `report.py`: Contains functions to create and save the final summary. It keeps reporting separate from calculations.
- `config.py`: Stores the API URL, timeout, and output path. It keeps all settings in one place.
- `__init__.py`: Makes the main classes available for import. It makes the package easier to use.
- `main.py`: Runs the program by connecting the other modules. It keeps the main program simple.

## What moved where

| Lab 02 function | Lab 03 location |
|---|---|
| `fetch_weather_records()` | `fetch()` in the `WeatherSource` class in `sources.py`. It gets weather data and creates `WeatherRecord` objects. |
| `calculate_daily_temperature()` | `calculate()` in the `TemperatureAggregation` class in `aggregations.py`. It calculates daily temperatures. Invalid values are now handled by `WeatherRecord` in `models.py`. |
| `calculate_daily_precipitation()` | `calculate()` in the `PrecipitationAggregation` class in `aggregations.py`. It calculates daily precipitation. Invalid values are now handled by `WeatherRecord` in `models.py`. |
| `build_summary()` | `build_summary()` in `report.py`. It creates the final summary and counts unique dates. |
| `write_summary()` | `write_summary()` in `report.py`. It saves the summary to a JSON file. |
| `main()` | `main()` in `main.py`. It connects the modules and runs the program. |

## Design choices

The WeatherRecord class represents one hourly weather record. It also handles missing and invalid values when a record is created.

The WeatherSource class gets weather data from the API and creates WeatherRecord objects. This keeps data collection separate from calculations.

The Aggregation class is the base class for weather calculations. It provides a common calculate() method that returns an empty dictionary by default. This allows different aggregation subclasses to use the same method name.

TemperatureAggregation and PrecipitationAggregation inherit from Aggregation. They both override the calculate() method. TemperatureAggregation calculates daily minimum, maximum, and mean temperatures. PrecipitationAggregation calculates daily total precipitation.

In report.py, a loop calls calculate() on both aggregation objects without checking their types. This is an example of polymorphism.

To add another subclass, I would create a new class that inherits from Aggregation and overrides the calculate() method. Then I would add the new class to the aggregation list in report.py.

## Known limitations

- Running the main program requires an internet connection, but the unit tests can run offline.
- The program counts unique dates but does not remove duplicate hourly weather records.
- The zip() function stops at the shortest list. If the API returns lists with different lengths, some records may be skipped. I would add a check to make sure the lists have the same length.
- Floating-point calculations may produce long decimal values, such as 10.799999999999999 instead of 10.8. I would use round() to make the results easier to read.