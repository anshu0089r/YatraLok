# YatraLok AI/ML Risk Prediction

## 1. Overview
Predicts tourist risk level (`LOW`, `MEDIUM`, `HIGH`) and generates explanations to assist police dashboard decision-making.

> **Important Limitation**: The AI model provides risk predictions based on movement, proximity, and historical area context. It does not replace human judgment; the final response decision always remains with the police officer.

## 2. Model Features (10 Features)
1. `distance_from_danger_zone`: Distance in meters from circular danger zone perimeter.
2. `distance_from_restricted_zone`: Distance in meters from restricted zone perimeter.
3. `speed`: Movement speed ($m/s$).
4. `time_of_day`: Local hour ($0 - 23$).
5. `duration_in_remote_area`: Consecutive minutes in remote region.
6. `movement_frequency`: Ratio of active movement intervals ($0.0 - 1.0$).
7. `route_deviation`: Lateral corridor deviation in meters.
8. `stationary_duration`: Consecutive minutes stationary ($< 0.1 m/s$).
9. `zone_entry_history`: Cumulative count of zone entries in trip.
10. `previous_incident_context`: Historical district crime rate per 100,000 population.

## 3. Files
- `data/dataset.csv`: 27,000 hybrid training records partitioned by whole-trip groups.
- `data/processed_data.csv`: Cleaned dataset ready for modeling.
- `preprocessing.py`: Cleans raw dataset and verifies splits.
- `feature_engineering.py`: Vectorizes features and produces transparent reason strings.
- `YatraLok_Risk_Model_Colab.ipynb`: Complete Google Colab / Jupyter notebook for cell-by-cell interactive training.
- `train.py`: Baseline model comparison and training script.
- `evaluate.py`: Test set evaluation script (Accuracy, Precision, Recall, F1, Confusion Matrix).
- `predict.py`: Real-time inference service with safe fallback.
