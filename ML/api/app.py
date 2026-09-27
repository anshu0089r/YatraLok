from flask import Flask, request, jsonify
from ML.geofencing.zone_checker import ZoneChecker
from ML.geofencing.geofence_service import GeofenceService

app = Flask(__name__)

# Initialize Geo-fence service
zone_checker = ZoneChecker()
geofence_service = GeofenceService(zone_checker)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "YatraLok AI/ML & Geo-Fencing API"}), 200


@app.route("/check-geofence", methods=["POST"])
def check_geofence():
    """
    Geo-fence checking endpoint.
    
    Request Body:
    {
        "tourist_id": "T-1001",           # optional (defaults to 'anonymous')
        "latitude": 28.6139,
        "longitude": 77.2090,
        "zones": [...]                    # optional custom zone list
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "Both 'latitude' and 'longitude' are required"}), 400

    try:
        lat = float(latitude)
        lon = float(longitude)
    except (ValueError, TypeError):
        return jsonify({"error": "'latitude' and 'longitude' must be numeric values"}), 400

    tourist_id = str(data.get("tourist_id", "default_tourist"))
    custom_zones = data.get("zones")

    result = geofence_service.process_location(
        tourist_id=tourist_id,
        latitude=lat,
        longitude=lon,
        zones=custom_zones,
    )

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
