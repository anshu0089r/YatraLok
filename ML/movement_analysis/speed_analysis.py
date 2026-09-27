import os
import sys
from typing import List, Optional
from datetime import datetime

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_CURRENT_DIR)
_ROOT_DIR = os.path.dirname(_ML_DIR)
for _p in [_ROOT_DIR, _ML_DIR, _CURRENT_DIR]:
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from ..geofencing.haversine import haversine_distance
except (ImportError, ValueError):
    try:
        from geofencing.haversine import haversine_distance
    except (ImportError, ValueError):
        from ML.geofencing.haversine import haversine_distance


def calculate_speed_from_coords(
    lat1: float,
    lon1: float,
    time1: datetime,
    lat2: float,
    lon2: float,
    time2: datetime,
) -> float:
    """
    Calculate average speed in meters per second (m/s) between two timestamped coordinates.
    """
    time_diff_sec = abs((time2 - time1).total_seconds())
    if time_diff_sec <= 0:
        return 0.0

    distance_meters = haversine_distance(lat1, lon1, lat2, lon2)
    return round(distance_meters / time_diff_sec, 2)


def calculate_stationary_duration(
    recent_speeds: List[float],
    stationary_threshold: float = 0.1,
    interval_minutes: float = 1.0,
) -> float:
    """
    Calculate consecutive minutes where speed was below stationary threshold.
    Resets to 0 if the latest point is moving.
    """
    if not recent_speeds:
        return 0.0

    consecutive_stops = 0
    for speed in reversed(recent_speeds):
        if speed < stationary_threshold:
            consecutive_stops += 1
        else:
            break

    return float(consecutive_stops * interval_minutes)


def calculate_movement_frequency(
    recent_speeds: List[float],
    window_size: int = 10,
    active_speed_threshold: float = 0.3,
) -> float:
    """
    Calculate fraction of the latest window_size observations with active movement.
    Range: [0.0, 1.0].
    """
    if not recent_speeds:
        return 1.0

    window = recent_speeds[-window_size:]
    if not window:
        return 1.0

    active_count = sum(1 for s in window if s >= active_speed_threshold)
    return round(active_count / len(window), 2)
