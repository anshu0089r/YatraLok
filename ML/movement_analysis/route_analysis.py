import os
import sys
from typing import List, Dict, Any, Optional

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


def calculate_route_deviation(
    current_lat: float,
    current_lon: float,
    planned_route: Optional[List[Dict[str, float]]] = None,
) -> float:
    """
    Calculate perpendicular / minimum distance in meters from the current GPS point
    to the nearest segment or waypoint on the planned route corridor.
    If no planned route is provided, returns 0.0.
    """
    if not planned_route or len(planned_route) == 0:
        return 0.0

    min_deviation = float("inf")
    for pt in planned_route:
        dist = haversine_distance(current_lat, current_lon, pt["latitude"], pt["longitude"])
        if dist < min_deviation:
            min_deviation = dist

    return round(min_deviation, 2) if min_deviation != float("inf") else 0.0


def calculate_remote_duration(
    recent_remote_flags: List[bool],
    interval_minutes: float = 1.0,
) -> float:
    """
    Calculate consecutive minutes spent inside a designated remote/isolated area.
    Resets to 0 once the tourist leaves the remote region.
    """
    if not recent_remote_flags:
        return 0.0

    consecutive_remote = 0
    for is_remote in reversed(recent_remote_flags):
        if is_remote:
            consecutive_remote += 1
        else:
            break

    return float(consecutive_remote * interval_minutes)
