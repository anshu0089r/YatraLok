# YatraLok — Geo-Fencing & AI/ML Safety Intelligence System

## 1. Problem Statement
Ensuring the safety of tourists traveling through unfamiliar terrain, wildlife sanctuaries, and restricted regions requires proactive, real-time safety monitoring. YatraLok integrates geo-fencing perimeter alerts with movement-anomaly detection to identify when a tourist might be approaching hazardous zones or exhibiting atypical movement behaviors.

---

## 2. Geo-Fencing Approach
YatraLok utilizes circular geo-fencing parameterized by center coordinates `(latitude, longitude)` and a protection `radius` in meters.
- **Zone Types**:
  - `DANGER`: Active hazardous zones (cliffs, rapid waters, wildlife corridors).
  - `RESTRICTED`: Protected forest reserves, military zones, or unauthorized sectors.
- **Event Tracking**:
  - `ZONE_ENTRY`: Detected when crossing from outside to inside a zone. Triggers an alert.
  - `ZONE_INSIDE`: Continuous stay inside the zone. Alert is suppressed to prevent notification spam.
  - `ZONE_EXIT`: Detected when crossing out of the zone perimeter.

---

## 3. Haversine Distance Formula
Great-circle distance on the spherical Earth surface ($R = 6,371,000 \text{ m}$):
$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)$$
$$c = 2 \cdot \text{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$
$$d = R \cdot c$$

---

## 4. Input Features (10 Model Features)
1. `distance_from_danger_zone`: Distance in meters from circular danger zone perimeter.
2. `distance_from_restricted_zone`: Distance in meters from restricted zone perimeter.
3. `speed`: Instantaneous/interval walking speed ($m/s$).
4. `time_of_day`: Local hour ($0 - 23$).
5. `duration_in_remote_area`: Consecutive minutes in remote/isolated coordinates.
6. `movement_frequency`: Fraction of recent time window with active movement ($0.0 - 1.0$).
7. `route_deviation`: Lateral perpendicular deviation from planned corridor ($m$).
8. `stationary_duration`: Consecutive minutes with speed $< 0.1\text{ m/s}$.
9. `zone_entry_history`: Cumulative count of zone crossings in the current trip.
10. `previous_incident_context`: Historical area-level IPC+SLL crime rate per 100,000 population.

---

## 5. Dataset & Preprocessing
- **Source**: 27,000 observations across 450 simulated trips based on 45 Tamil Nadu police district crime reporting areas (2022).
- **Splits**: Partitioned by whole trips (18,900 Train / 5,400 Validation / 2,700 Test).
- **Missing Value Imputation & Scaling**: Features are standard-scaled (`StandardScaler`) fitted exclusively on the training partition.

---

## 6. Model Training & Google Colab Workflow
Interactive training is organized in cell-by-cell format inside [`risk_prediction/YatraLok_Risk_Model_Colab.ipynb`](file:///c:/Users/rajan/OneDrive/Desktop/YatraLok_ML/ML/risk_prediction/YatraLok_Risk_Model_Colab.ipynb):
1. **Logistic Regression** (Linear baseline with class weighting).
2. **Decision Tree Classifier** (Interpretable tree baseline).
3. **Random Forest Classifier** (Ensemble tree classifier with robust generalization).

---

## 7. Model Evaluation
Models are evaluated across key classification metrics on the unseen test set:
- **Accuracy**
- **Precision (Weighted)**
- **Recall (Weighted)**
- **F1-Score (Weighted)**
- **Confusion Matrix** (Rows: Actual `[LOW, MEDIUM, HIGH]`, Columns: Predicted)

---

## 8. API Specification

### 8.1 Geo-fence Check: `POST /check-geofence`
**Request:**
```json
{
  "tourist_id": "T-1001",
  "latitude": 28.6139,
  "longitude": 77.2090
}
```
**Response:**
```json
{
  "inside_zone": true,
  "zone_name": "Restricted Forest Area",
  "zone_type": "RESTRICTED",
  "distance": 42.0,
  "warning": true,
  "event": "ZONE_ENTRY"
}
```

### 8.2 Risk Prediction: `POST /predict-risk`
**Request:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "speed": 2.5,
  "time_of_day": 23,
  "distance_from_danger_zone": 120,
  "route_deviation": 150
}
```
**Response:**
```json
{
  "risk_score": 0.76,
  "risk_level": "HIGH",
  "reason": "Tourist movement is close to a restricted zone and shows unusual route deviation."
}
```

---

## 9. Important Limitations & Safety Disclaimer
> **Do NOT claim**: "AI detects real danger with 100% accuracy."
> 
> **Standard Safety Principle**:
> "AI provides an advisory risk prediction based on available movement and location features. The primary SOS mechanism operates independently, and the final response decision remains with human police officers."
