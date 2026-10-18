class WeatherRecord:
    """Represent one hourly weather record and clean invalid values."""

    def __init__(self, time, temperature, precipitation):
        self.time = time
        self.date = time.split("T")[0]

        try:
            self.temperature = float(temperature)
        except (TypeError, ValueError):
            self.temperature = None

        try:
            precipitation = float(precipitation)

            if precipitation < 0:
                self.precipitation = None
            else:
                self.precipitation = precipitation

        except (TypeError, ValueError):
            self.precipitation = None

    def __str__(self):
        return f"{self.date}: temperature={self.temperature}, precipitation={self.precipitation}"
