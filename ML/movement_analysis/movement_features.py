import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_CURRENT_DIR)
_ROOT_DIR = os.path.dirname(_ML_DIR)
for _p in [_ROOT_DIR, _ML_DIR, _CURRENT_DIR]:
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from ..geofencing.zone_checker import ZoneChecker
    from .speed_analysis import (
        calculate_speed_from_coords,
        calculate_stationary_duration,
        calculate_movement_frequency,
    )
    from .route_analysis import calculate_route_deviation, calculate_remote_duration
except (ImportError, ValueError):
    try:
        from geofencing.zone_checker import ZoneChecker
        from speed_analysis import (
            calculate_speed_from_coords,
            calculate_stationary_duration,
            calculate_movement_frequency,
        )
        from route_analysis import calculate_route_deviation, calculate_remote_duration
    except (ImportError, ValueError):
        from ML.geofencing.zone_checker import ZoneChecker
        from ML.movement_analysis.speed_analysis import (
            calculate_speed_from_coords,
            calculate_stationary_duration,
            calculate_movement_frequency,
        )
        from ML.movement_analysis.route_analysis import calculate_route_deviation, calculate_remote_duration


class MovementFeatureExtractor:
    """
    Extracts structured AI/ML movement features from GPS trajectory points and trip context.
    """

    def __init__(self, zone_checker: Optional[ZoneChecker] = None):
        self.zone_checker = zone_checker or ZoneChecker()

    def extract_features(
        self,
        current_location: Dict[str, Any],
        location_history: Optional[List[Dict[str, Any]]] = None,
        planned_route: Optional[List[Dict[str, float]]] = None,
        zones: Optional[List[Dict[str, Any]]] = None,
        previous_incident_context: float = 350.0,
    ) -> Dict[str, float]:
        """
        Extract the 10 feature values needed by the Risk Prediction model.

        Features:
        1. distance_from_danger_zone
        2. distance_from_restricted_zone
        3. speed
        4. time_of_day (0 - 23)
        5. duration_in_remote_area
        6. movement_frequency
        7. route_deviation
        8. stationary_duration
        9. zone_entry_history
        10. previous_incident_context
        """
        lat = float(current_location["latitude"])
        lon = float(current_location["longitude"])
        speed = float(current_location.get("speed", 0.0))

        # Time of day
        ts = current_location.get("timestamp")
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                time_of_day = float(dt.hour)
            except Exception:
                time_of_day = 12.0
        elif isinstance(ts, datetime):
            time_of_day = float(ts.hour)
        else:
            time_of_day = float(current_location.get("time_of_day", 12.0))

        # Zone proximity
        zone_result = self.zone_checker.check_location(lat, lon, zones)
        danger_dist = zone_result.get("distance_from_danger_zone", 999.0)
        restricted_dist = zone_result.get("distance_from_restricted_zone", 999.0)

        # Process history for speed, stationary, frequency, and zone entry history
        history = location_history or []
        speeds: List[float] = []
        remote_flags: List[bool] = []
        zone_entry_count = 0

        for pt in history:
            if "speed" in pt:
                speeds.append(float(pt["speed"]))
            if "is_remote" in pt:
                remote_flags.append(bool(pt["is_remote"]))

        if not speeds and "speed" in current_location:
            speeds.append(speed)

        stationary_dur = calculate_stationary_duration(speeds)
        move_freq = calculate_movement_frequency(speeds)
        remote_dur = calculate_remote_duration(remote_flags)
        deviation = calculate_route_deviation(lat, lon, planned_route)
        zone_entry_history = float(current_location.get("zone_entry_history", zone_entry_count))

        return {
            "distance_from_danger_zone": float(danger_dist),
            "distance_from_restricted_zone": float(restricted_dist),
            "speed": float(speed),
            "time_of_day": float(time_of_day),
            "duration_in_remote_area": float(remote_dur),
            "movement_frequency": float(move_freq),
            "route_deviation": float(deviation),
            "stationary_duration": float(stationary_dur),
            "zone_entry_history": float(zone_entry_history),
            "previous_incident_context": float(previous_incident_context),
        }
