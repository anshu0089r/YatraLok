import csv
from typing import List, Dict, Tuple, Any

FEATURE_COLUMNS = [
    "distance_from_danger_zone",
    "distance_from_restricted_zone",
    "speed",
    "time_of_day",
    "duration_in_remote_area",
    "movement_frequency",
    "route_deviation",
    "stationary_duration",
    "zone_entry_history",
    "previous_incident_context",
]

TARGET_COLUMN = "risk_level"


def clean_row(row: Dict[str, str]) -> Dict[str, Any]:
    """
    Clean, validate, and convert a single row of features.
    """
    cleaned: Dict[str, Any] = {}
    for col in FEATURE_COLUMNS:
        val = row.get(col, "0")
        try:
            cleaned[col] = float(val) if val != "" else 0.0
        except ValueError:
            cleaned[col] = 0.0

    cleaned[TARGET_COLUMN] = row.get(TARGET_COLUMN, "LOW").strip().upper()
    cleaned["dataset_split"] = row.get("dataset_split", "train").strip().lower()
    cleaned["trip_id"] = row.get("trip_id", "")
    return cleaned


def preprocess_dataset(
    input_path: str = "ML/risk_prediction/data/dataset.csv",
    output_path: str = "ML/risk_prediction/data/processed_data.csv",
) -> Dict[str, int]:
    """
    Read raw dataset.csv, clean values, handle missing data,
    and save the clean processed_data.csv.
    """
    rows: List[Dict[str, Any]] = []
    split_counts = {"train": 0, "validation": 0, "test": 0}

    with open(input_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cleaned = clean_row(r)
            rows.append(cleaned)
            split = cleaned.get("dataset_split", "train")
            split_counts[split] = split_counts.get(split, 0) + 1

    fieldnames = FEATURE_COLUMNS + [TARGET_COLUMN, "dataset_split", "trip_id"]
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return split_counts


if __name__ == "__main__":
    counts = preprocess_dataset()
    print("Preprocessing completed successfully!")
    print("Split breakdown:", counts)
