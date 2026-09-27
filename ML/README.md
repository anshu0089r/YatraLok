# YatraLok — Geo-Fencing & AI/ML Safety Intelligence System

## 1. Overview
This module (`ML`) provides real-time geo-fencing safety checks and AI-powered risk assessment for the YatraLok tourist safety platform.

> **Important Safety Notice**: AI does **not** decide if a tourist is definitely in danger. AI only provides a risk prediction score and advisory level (`LOW`, `MEDIUM`, `HIGH`) to assist police authorities in prioritizing attention. The primary SOS mechanism operates independently and remains functional even if the AI service is unavailable.

---

## 2. Project Structure
```text
ML/
│
├── geofencing/
│   ├── haversine.py
│   ├── zone_checker.py
│   ├── geofence_service.py
│   └── README.md
│
├── risk_prediction/
│   ├── data/
│   │   ├── dataset.csv
│   │   └── processed_data.csv
│   │
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── model.pkl
│   └── README.md
│
├── movement_analysis/
│   ├── speed_analysis.py
│   ├── route_analysis.py
│   └── movement_features.py
│
├── api/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. Offline Location & GPS Data Contract (Member 4 Specification)

When a tourist enters an area with no internet connectivity:
```text
GPS Sensor → Local Mobile Cache (SQLite/AsyncStorage)
      ↓ (Network Offline)
Batch Locally Stored Points
      ↓ (Network Restored)
HTTP Sync to Backend → Stored in MySQL → Forwarded to AI/ML Module for Historical Trajectory Processing
```

### 3.1 Standard GPS Point Schema
Frontend and Backend should adhere to this JSON format for each location point:

```json
{
  "tourist_id": "T-1001",
  "trip_id": "TRIP-2026-001",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "accuracy": 5.0,
  "speed": 1.2,
  "timestamp": "2026-09-27T10:15:30+05:30"
}
```

### 3.2 Offline Batch Sync Payload (Mobile → Backend → AI/ML)
When connectivity resumes, mobile pushes queued records chronologically:

```json
{
  "tourist_id": "T-1001",
  "trip_id": "TRIP-2026-001",
  "sync_timestamp": "2026-09-27T10:45:00+05:30",
  "locations": [
    {
      "latitude": 28.6139,
      "longitude": 77.2090,
      "speed": 1.2,
      "timestamp": "2026-09-27T10:15:30+05:30"
    },
    {
      "latitude": 28.6145,
      "longitude": 77.2105,
      "speed": 1.4,
      "timestamp": "2026-09-27T10:16:30+05:30"
    }
  ]
}
```

---

## 4. Environment & Installation

```bash
cd ML
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```
