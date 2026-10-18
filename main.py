from weathersummary.report import build_summary, write_summary
from weathersummary.sources import WeatherSource


def main():
    """Run the weather data aggregation program."""

    source = WeatherSource()
    records = source.fetch()

    if records is None:
        return

    summary = build_summary(records)
    write_summary(summary)


if __name__ == "__main__":
    main()
