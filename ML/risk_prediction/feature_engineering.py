from typing import List, Dict, Any, Tuple

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

LABEL_TO_INT = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
INT_TO_LABEL = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
TARGET_COLUMN = "risk_level"


def row_to_feature_vector(row: Dict[str, Any]) -> List[float]:
    """
    Extract ordered feature values as a numeric vector.
    """
    return [float(row.get(col, 0.0)) for col in FEATURE_COLUMNS]


def generate_risk_explanation(features: Dict[str, float], risk_level: str) -> str:
    """
    Generate transparent, human-readable safety reasoning for police dashboard.
    """
    reasons = []

    danger_dist = features.get("distance_from_danger_zone", 999.0)
    restricted_dist = features.get("distance_from_restricted_zone", 999.0)
    dev = features.get("route_deviation", 0.0)
    remote_dur = features.get("duration_in_remote_area", 0.0)
    stationary_dur = features.get("stationary_duration", 0.0)
    hour = features.get("time_of_day", 12.0)
    move_freq = features.get("movement_frequency", 1.0)
    crime_rate = features.get("previous_incident_context", 0.0)

    if danger_dist <= 0:
        reasons.append("tourist is currently inside an active danger zone")
    elif danger_dist < 100:
        reasons.append(f"tourist is within {danger_dist:.0f}m of a danger zone")

    if restricted_dist <= 0:
        reasons.append("tourist has entered a restricted zone")
    elif restricted_dist < 100:
        reasons.append(f"tourist is within {restricted_dist:.0f}m of a restricted zone")

    if dev > 200:
        reasons.append(f"route deviation of {dev:.0f}m from planned corridor")

    if remote_dur > 5:
        reasons.append(f"sustained stay of {remote_dur:.0f} mins in remote area")

    if stationary_dur > 10:
        reasons.append(f"prolonged stationary duration of {stationary_dur:.0f} mins")

    if (hour >= 22 or hour < 5) and (danger_dist < 200 or restricted_dist < 200 or remote_dur > 0):
        reasons.append("late-night movement in isolated/sensitive proximity")

    if not reasons:
        if risk_level == "HIGH":
            return "Multiple compounding movement anomalies detected."
        elif risk_level == "MEDIUM":
            return "Moderate deviation or proximity to alert perimeter observed."
        else:
            return "Normal tourist movement within expected safety corridors."

    return "Risk indicators: " + "; ".join(reasons) + "."
