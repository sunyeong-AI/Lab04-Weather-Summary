class WeatherRecord:
    """Represent one hourly weather record and clean invalid values."""

    def __init__(
        self,
        time: str,
        temperature: str | float | None,
        precipitation: str | float | None,
    ) -> None:
        self.time = time
        self.date = time.split("T")[0]

        self.temperature: float | None = None
        self.precipitation: float | None = None

        try:
            self.temperature = float(temperature) if temperature is not None else None
        except (TypeError, ValueError):
            self.temperature = None

        try:
            precipitation_value = (
                float(precipitation) if precipitation is not None else None
            )

            if precipitation_value is not None and precipitation_value >= 0:
                self.precipitation = precipitation_value

        except (TypeError, ValueError):
            self.precipitation = None

    def __str__(self) -> str:
        return (
            f"{self.date}: temperature={self.temperature}, "
            f"precipitation={self.precipitation}"
        )
