"""Simple sensor-reading utilities.

Starting point for the Python check. Read it, run it with `python starter.py`,
then work through the tasks in TASKS.md in order.

The code here already follows the standard we expect from you: type hints and a
short docstring on every function. Match that bar in everything you add, and
keep the program runnable after each task.
"""
# This program gives a summary of sensors and readings information.
import pandas as pd
from matplotlib import pyplot as plt

# Loads sensor readings data
data = pd.read_csv("data.csv")


class Sensor:
    """Base class that provides sensor information."""

    def __init__(self, name: str, unit: str) -> None:
        """Initialize a new sensor."""
        self.name = name
        self.unit = unit

    def summary(self, readings: list[float]) -> dict[str, int | float | str |
                                                    list[float]]:
        """Return summary of sensor reading. Take readings and temperature threshold."""
        if len(readings) != 0:
            return {"count": len(readings), "min": min(readings), "max": max(readings),
                    "mean": round(average(readings), 2),
                    "readings_above": readings_above(readings)}
        else:
            return {"count": len(readings), "min": "No data", "max": "No data",
                    "mean": "No data",
                    "readings_above": "No data"}


class TemperatureSensor(Sensor):
    """Converts Celsius temperatures to Fahrenheit. Child class of sensor."""

    def to_fahrenheit(self, readings: list[float]) -> list[float]:
        """Return converted Celsius temperature to Fahrenheit."""
        return [reading * 9 / 5 + 32 for reading in readings]


class PressureSensor(Sensor):
    """Counts how many readings are out of temperature range."""

    def summary(self, readings: list[float]) -> dict[str, int | float | str |
                                                    list[float]]:
        """Count how many readings are below 90F and above 110F."""
        base = super().summary(readings)
        count = 0
        for reading in readings:
            if reading < 90 or reading > 110:
                count += 1
        base["out_of_range"] = count
        return base


def summarize(readings: list[float]) -> dict[str, int | float | None |
                                            str | list[float]]:
    """Return dictionary for readings information."""
    if len(readings) != 0:
        return {"count": len(readings), "min": min(readings),
                "max": max(readings),
                "mean": average(readings),
                "above_21": readings_above(readings)}
    else:
        return {"count": len(readings), "min": "No data", "max": "No data",
                "mean": "No data",
                "readings_above": "No data"}


def sensor_temperature_raw(dataframe: pd.DataFrame[str, float], column1: str,
                           column2: str, sensor: str) -> pd.DataFrame[str, float]:
    """Return average temperature per sensor."""
    sensors = dataframe.groupby(column1)[column2].apply(list)
    return sensors[sensor]


def sensor_temperature(dataframe: pd.DataFrame[str, float], column1: str,
                       column2: str, sensor: str) -> pd.DataFrame[str, float]:
    """Return average temperature per sensor."""
    sensors = dataframe.groupby(column1)[column2].mean()
    return sensors[sensor]


def readings_above(readings: list[float]) -> list[float]:
    """Return readings that meet a threshold."""
    return [reading for reading in readings if reading > 21]


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + 32


def average(readings: list[float]) -> float | None:
    """Return the arithmetic mean of a non-empty list of readings."""
    try:
        return sum(readings) / len(readings)

    except ZeroDivisionError:
        return None


def readings_range(readings: list[float]) -> float | None:
    """Return the difference between highest and lowest readings."""
    try:
        return max(readings) - min(readings)

    except ValueError:
        return None


def main() -> None:
    """Print a short summary of a sample batch of readings."""
    readings = [20.5, 21.0, 19.8, 22.3, 20.1]

    # Main readings summaries
    print("Number of readings:", len(readings))
    # Stops unexpected crash if 0 readings. Can't return 0 since that is a temperature.
    if average(readings) is None or readings_range(readings) is None:
        print("Average temperature (C): No data")
        print("Temperature range (C): No data")
    else:
        print("Average temperature (C):", round(average(readings), 2))
        print("Temperature range (C):", round(readings_range(readings), 2))
    print("Temperature readings (F):", str([celsius_to_fahrenheit(celsius=reading)
                                            for reading in readings]).strip("[]")
          )
    print(summarize(readings))
    print()  # Add break for CLI readability.

    # Sensor and summary loop
    main_sensor = Sensor(name="main_sensor", unit="C")
    temperature_sensor = TemperatureSensor(name="temperature_sensor", unit="F")
    pressure_sensor = PressureSensor(name="pressure_sensor", unit="C")
    sensors = [main_sensor, temperature_sensor, pressure_sensor]
    for sensor in sensors:
        print("Sensor name: ", sensor.name)
        print("Sensor unit: ", sensor.unit)
        if sensor == temperature_sensor:
            fahrenheit_readings = temperature_sensor.to_fahrenheit(readings)
            print("Temperatures (F): ", fahrenheit_readings)
        else:
            print("Readings summary: ", sensor.summary(readings=readings))
        print()  # Add break inbetween each entry for CLI readability.

    # CSV file average temperature readings
    print("Average temperature (C):", round(data["temperature_c"].mean(), 2))

    print("Average temperature of sensor A (C):", round(sensor_temperature
                                                        (dataframe=data,
                                                         column1="sensor_id",
                                                         column2="temperature_c",
                                                         sensor="sensor_A"), 2))
    print("Average temperature of sensor B (C):", round(sensor_temperature
                                                        (dataframe=data,
                                                         column1="sensor_id",
                                                         column2="temperature_c",
                                                         sensor="sensor_B"), 2))

    timestamp: pd.Series = data.groupby("sensor_id")["timestamp"].apply(list)

    # Graph plotting
    fig, ax = plt.subplots()
    ax.plot(timestamp["sensor_A"], sensor_temperature_raw(dataframe=data,
                                                          column1="sensor_id",
                                                          column2="temperature_c",
                                                          sensor="sensor_A"),
            label="Sensor A")

    ax.plot(timestamp["sensor_B"], sensor_temperature_raw(dataframe=data,
                                                          column1="sensor_id",
                                                          column2="temperature_c",
                                                          sensor="sensor_B"),
            label="Sensor B")

    # Graph styling
    ax.set_title("Temperatures of Sensors")
    ax.set_ylabel("Temperature (C)")
    ax.set_xlabel("Time")
    ax.grid()
    ax.margins(x=0.001)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
