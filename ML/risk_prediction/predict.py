import os
from typing import Dict, Any, Optional
from .feature_engineering import (
    FEATURE_COLUMNS,
    row_to_feature_vector,
    generate_risk_explanation,
)


class RiskPredictor:
    """
    Inference service for predicting tourist safety risk levels (LOW, MEDIUM, HIGH)
    and generating transparent reasons for the police dashboard.
    """

    def __init__(self, model_path: str = "ML/risk_prediction/model.pkl"):
        self.model_path = model_path
        self.model_payload: Optional[Dict[str, Any]] = None
        self._load_model()

    def _load_model(self) -> None:
        """Attempt to load saved model artifact."""
        if os.path.exists(self.model_path):
            try:
                import joblib
                self.model_payload = joblib.load(self.model_path)
            except Exception as e:
                print(f"Notice: Model could not be loaded from {self.model_path}: {e}")
                self.model_payload = None

    def predict(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict risk score and risk level from movement and location features.
        """
        # Ensure all 10 features exist with floats
        clean_features: Dict[str, float] = {}
        for col in FEATURE_COLUMNS:
            clean_features[col] = float(feature_data.get(col, 0.0))

        # 1. Model Inference (if model artifact is loaded)
        if self.model_payload and "model" in self.model_payload:
            try:
                model = self.model_payload["model"]
                vec = [row_to_feature_vector(clean_features)]
                pred_label = str(model.predict(vec)[0])
                
                # Extract confidence probability if classifier supports predict_proba
                if hasattr(model, "predict_proba"):
                    probs = model.predict_proba(vec)[0]
                    classes = list(self.model_payload.get("classes", model.classes_))
                    idx = classes.index(pred_label) if pred_label in classes else 0
                    risk_score = float(probs[idx])
                else:
                    score_map = {"LOW": 0.25, "MEDIUM": 0.55, "HIGH": 0.85}
                    risk_score = score_map.get(pred_label, 0.5)

                reason = generate_risk_explanation(clean_features, pred_label)
                return {
                    "risk_score": round(risk_score, 2),
                    "risk_level": pred_label,
                    "reason": reason,
                }
            except Exception as e:
                print(f"Notice: Inference encountered error, falling back to rule engine: {e}")

        # 2. Rule-based Safety Fallback (Guarantees zero downtime)
        return self._rule_based_fallback(clean_features)

    def _rule_based_fallback(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Rule-based heuristic risk scoring used when ML model artifact is offline.
        """
        danger_dist = features.get("distance_from_danger_zone", 999.0)
        restricted_dist = features.get("distance_from_restricted_zone", 999.0)
        dev = features.get("route_deviation", 0.0)
        remote = features.get("duration_in_remote_area", 0.0)
        hour = features.get("time_of_day", 12.0)
        stat = features.get("stationary_duration", 0.0)

        score = 0.0
        if danger_dist <= 0:
            score += 0.35
        elif danger_dist < 100:
            score += 0.20

        if restricted_dist <= 0:
            score += 0.40
        elif restricted_dist < 100:
            score += 0.25

        if dev > 300:
            score += 0.15

        if remote > 5:
            score += 0.10

        if (hour >= 22 or hour < 5) and (danger_dist < 200 or restricted_dist < 200):
            score += 0.15

        if stat > 15:
            score += 0.10

        score = min(1.0, score)

        if score >= 0.55:
            level = "HIGH"
        elif score >= 0.25:
            level = "MEDIUM"
        else:
            level = "LOW"

        reason = generate_risk_explanation(features, level)
        return {
            "risk_score": round(score, 2),
            "risk_level": level,
            "reason": reason,
        }
