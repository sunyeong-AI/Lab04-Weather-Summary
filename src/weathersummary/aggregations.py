class Aggregation:
    """Base class for weather aggregations."""

    def calculate(self, records):
        """Return aggregation results."""
        return {}


class TemperatureAggregation(Aggregation):
    """Calculate daily temperature statistics."""

    def calculate(self, records):
        """Calculate daily minimum, maximum, and mean temperatures."""

        daily_temperatures = {}

        for record in records:
            if record.temperature is None:
                continue

            date = record.date

            if date not in daily_temperatures:
                daily_temperatures[date] = []

            daily_temperatures[date].append(record.temperature)

        daily_temp_stats = {}

        for date, temperatures in daily_temperatures.items():
            minimum = min(temperatures)
            maximum = max(temperatures)
            mean = sum(temperatures) / len(temperatures)

            daily_temp_stats[date] = {
                "min": minimum,
                "max": maximum,
                "mean": mean
            }

        return daily_temp_stats


class PrecipitationAggregation(Aggregation):
    """Calculate daily precipitation totals."""

    def calculate(self, records):
        """Calculate total precipitation for each day."""

        daily_precipitations = {}

        for record in records:
            if record.precipitation is None:
                continue

            date = record.date

            if date not in daily_precipitations:
                daily_precipitations[date] = []

            daily_precipitations[date].append(record.precipitation)

        daily_precip_totals = {}

        for date, precipitations in daily_precipitations.items():
            total_precipitation = sum(precipitations)
            daily_precip_totals[date] = total_precipitation

        return daily_precip_totals