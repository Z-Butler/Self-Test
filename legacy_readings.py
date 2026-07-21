"""Provides summary for anomalies found and the corresponding times."""
import statistics


def parse_reading(entry: str) -> tuple[str, float]:
    """Separate times and anomalies. Convert anomaly entry into float."""
    entry = entry.split(",")
    time_saved = entry[0]
    anomaly_value = float(entry[1])
    return time_saved, anomaly_value


def load(entries: list[str]) -> list[str]:
    """Filter entries with no data."""
    output = []
    for i in range(len(entries)):
        entry = entries[i].strip()
        if entry == "":
            continue
        output.append(parse_reading(entry))
    return output


def find_anomalies(recordings: list, limit: int) -> list:
    """Return a list of anomalies found in records."""
    anomaly_list = []
    for recording in recordings:
        if recording[1] > limit:
            anomaly_list.append(recording)
    return anomaly_list


def mean_value(records: list[str]) -> float:
    """Return mean value of records."""
    values = []
    for record in records:
        values.append(record[1])
    try:
        return statistics.mean(values)
    except ValueError:
        return 0


def main() -> None:
    """Print summary and findings of anomalies."""
    raw = ["00:00,20.1", "01:00,25.4", "  ", "02:00,19.8", "03:00,31.2"]
    recordings = load(raw)
    print("count", len(recordings))
    print("mean", mean_value(recordings))
    print("anomalies", find_anomalies(recordings, 25))


if __name__=="__main__":
    main()
