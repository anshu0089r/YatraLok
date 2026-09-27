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
    from .haversine import haversine_distance
except (ImportError, ValueError):
    try:
        from geofencing.haversine import haversine_distance
    except (ImportError, ValueError):
        from ML.geofencing.haversine import haversine_distance


class ZoneChecker:
    """
    Circular Geo-fencing zone checker for tourist safety.
    """

    WARNING_ZONE_TYPES = {"DANGER", "RESTRICTED"}

    def __init__(self, zones: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize with a list of active zones.
        
        Each zone dictionary format:
        {
            "zone_id": str,
            "zone_name": str,
            "latitude": float,
            "longitude": float,
            "radius": float,  # in meters
            "zone_type": "DANGER" | "RESTRICTED"
        }
        """
        self.zones: List[Dict[str, Any]] = zones or []

    def set_zones(self, zones: List[Dict[str, Any]]) -> None:
        """Update active zones."""
        self.zones = zones

    def check_location(
        self, latitude: float, longitude: float, zones: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Check tourist location against active zones.

        Returns:
            Dict containing inside status, triggered zone info, distance, and nearest zones.
        """
        active_zones = zones if zones is not None else self.zones

        inside_zone = False
        matched_zone_name: Optional[str] = None
        matched_zone_type: Optional[str] = None
        matched_distance: Optional[float] = None
        warning = False

        nearest_danger_dist = float("inf")
        nearest_restricted_dist = float("inf")

        for zone in active_zones:
            zone_lat = zone["latitude"]
            zone_lon = zone["longitude"]
            radius = zone["radius"]
            z_type = zone.get("zone_type", "").upper()

            dist = haversine_distance(latitude, longitude, zone_lat, zone_lon)

            # Track nearest danger & restricted zones (boundary distance: dist - radius)
            boundary_dist = max(0.0, dist - radius)
            if z_type == "DANGER" and boundary_dist < nearest_danger_dist:
                nearest_danger_dist = boundary_dist
            elif z_type == "RESTRICTED" and boundary_dist < nearest_restricted_dist:
                nearest_restricted_dist = boundary_dist

            # Check if inside circular zone
            if dist <= radius:
                inside_zone = True
                matched_zone_name = zone.get("zone_name", "Unknown Zone")
                matched_zone_type = z_type
                matched_distance = round(dist, 2)

                if z_type in self.WARNING_ZONE_TYPES:
                    warning = True

        return {
            "inside_zone": inside_zone,
            "zone_name": matched_zone_name,
            "zone_type": matched_zone_type,
            "distance": matched_distance,
            "warning": warning,
            "distance_from_danger_zone": round(nearest_danger_dist, 2) if nearest_danger_dist != float("inf") else -1.0,
            "distance_from_restricted_zone": round(nearest_restricted_dist, 2) if nearest_restricted_dist != float("inf") else -1.0,
        }
