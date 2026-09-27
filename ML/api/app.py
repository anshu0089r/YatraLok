from flask import Flask, request, jsonify
from ML.geofencing.zone_checker import ZoneChecker
from ML.geofencing.geofence_service import GeofenceService
from ML.movement_analysis.movement_features import MovementFeatureExtractor
from ML.risk_prediction.predict import RiskPredictor

app = Flask(__name__)

# Initialize Geo-fencing & AI/ML components
zone_checker = ZoneChecker()
geofence_service = GeofenceService(zone_checker)
feature_extractor = MovementFeatureExtractor(zone_checker)
risk_predictor = RiskPredictor()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "YatraLok AI/ML & Geo-Fencing API",
        "model_loaded": risk_predictor.model_payload is not None,
    }), 200


@app.route("/check-geofence", methods=["POST"])
def check_geofence():
    """
    Circular Geo-fence checking endpoint with alert deduplication.
    
    Request Body:
    {
        "tourist_id": "T-1001",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "zones": [...]
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


@app.route("/predict-risk", methods=["POST"])
def predict_risk():
    """
    AI/ML Tourist Risk Prediction endpoint.
    
    Accepts either direct feature dictionary or raw GPS location with trip context:
    {
        "latitude": 28.61,
        "longitude": 77.23,
        "speed": 2.5,
        "time_of_day": 23,
        "distance_from_danger_zone": 120,
        "route_deviation": 1,
        "previous_incident_context": 350
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    # If raw GPS point coordinates are provided without pre-computed distances, extract features
    if "latitude" in data and "longitude" in data and "distance_from_danger_zone" not in data:
        features = feature_extractor.extract_features(
            current_location=data,
            location_history=data.get("location_history"),
            planned_route=data.get("planned_route"),
            zones=data.get("zones"),
            previous_incident_context=float(data.get("previous_incident_context", 350.0)),
        )
    else:
        features = data

    prediction = risk_predictor.predict(features)
    return jsonify(prediction), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
