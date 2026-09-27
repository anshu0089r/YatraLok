import os
import sys
from typing import Dict, List, Optional, Any

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.dirname(_CURRENT_DIR)
_ROOT_DIR = os.path.dirname(_ML_DIR)
for _p in [_ROOT_DIR, _ML_DIR, _CURRENT_DIR]:
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from .zone_checker import ZoneChecker
    from .haversine import haversine_distance
except (ImportError, ValueError):
    try:
        from geofencing.zone_checker import ZoneChecker
        from geofencing.haversine import haversine_distance
    except (ImportError, ValueError):
        from ML.geofencing.zone_checker import ZoneChecker
        from ML.geofencing.haversine import haversine_distance


class GeofenceService:
    """
    Stateful Geo-fence service that tracks tourist movements,
    detects entry/exit transitions, and manages alert de-duplication.
    """

    def __init__(self, zone_checker: Optional[ZoneChecker] = None):
        self.zone_checker = zone_checker or ZoneChecker()
        # Map of tourist_id -> set of active zone_ids they are currently inside
        self.tourist_active_zones: Dict[str, set] = {}

    def set_zones(self, zones: List[Dict[str, Any]]) -> None:
        """Update active safety zones in the system."""
        self.zone_checker.set_zones(zones)

    def process_location(
        self,
        tourist_id: str,
        latitude: float,
        longitude: float,
        zones: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate a tourist's coordinate, determine entry/exit state transitions,
        and generate warnings without repeated alerts for continuous presence.
        """
        active_zones = zones if zones is not None else self.zone_checker.zones
        check_result = self.zone_checker.check_location(latitude, longitude, active_zones)

        previous_zones = self.tourist_active_zones.get(tourist_id, set())
        current_zones = set()

        # Find all zone_ids tourist is currently inside
        for zone in active_zones:
            dist = haversine_distance(latitude, longitude, zone["latitude"], zone["longitude"])
            if dist <= zone["radius"]:
                current_zones.add(zone.get("zone_id", zone.get("zone_name", "unknown")))

        # Determine transitions
        entered_zones = current_zones - previous_zones
        exited_zones = previous_zones - current_zones

        # Update tracked state
        self.tourist_active_zones[tourist_id] = current_zones

        # Determine event type
        if entered_zones:
            event = "ZONE_ENTRY"
            should_warn = check_result["warning"]
        elif exited_zones and not current_zones:
            event = "ZONE_EXIT"
            should_warn = False
        elif current_zones:
            event = "ZONE_INSIDE"
            should_warn = False  # Suppress repeated continuous alert
        else:
            event = "OUTSIDE"
            should_warn = False

        return {
            "tourist_id": tourist_id,
            "inside_zone": check_result["inside_zone"],
            "zone_name": check_result["zone_name"],
            "zone_type": check_result["zone_type"],
            "distance": check_result["distance"],
            "warning": should_warn,
            "event": event,
            "entered_zones": list(entered_zones),
            "exited_zones": list(exited_zones),
            "distance_from_danger_zone": check_result["distance_from_danger_zone"],
            "distance_from_restricted_zone": check_result["distance_from_restricted_zone"],
        }
