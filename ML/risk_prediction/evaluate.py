import os
from typing import Dict, Any

try:
    from .train import load_split_data
    from .feature_engineering import FEATURE_COLUMNS
except ImportError:
    try:
        from ML.risk_prediction.train import load_split_data
        from ML.risk_prediction.feature_engineering import FEATURE_COLUMNS
    except ImportError:
        from train import load_split_data
        from feature_engineering import FEATURE_COLUMNS


def _resolve_path(path: str, filename: str) -> str:
    if os.path.exists(path):
        return path
    local = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(local):
        return local
    return path


def evaluate_saved_model(
    model_path: str = "ML/risk_prediction/model.pkl",
    data_path: str = "ML/risk_prediction/data/processed_data.csv",
) -> Dict[str, Any]:
    """
    Evaluate the saved serialized model on the held-out test split.
    """
    model_path = _resolve_path(model_path, "model.pkl")
    data_path = _resolve_path(data_path, os.path.join("data", "processed_data.csv"))
    try:
        import joblib
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            confusion_matrix,
            classification_report,
        )
    except ImportError as e:
        print(f"Warning: Evaluation packages not available: {e}")
        return {}

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    payload = joblib.load(model_path)
    model = payload["model"]

    _, _, _, _, X_test, y_test = load_split_data(data_path)

    try:
        import pandas as pd
        X_test_input = pd.DataFrame(X_test, columns=FEATURE_COLUMNS)
    except Exception:
        X_test_input = X_test

    test_preds = model.predict(X_test_input)

    acc = accuracy_score(y_test, test_preds)
    prec = precision_score(y_test, test_preds, average="weighted")
    rec = recall_score(y_test, test_preds, average="weighted")
    f1 = f1_score(y_test, test_preds, average="weighted")
    cm = confusion_matrix(y_test, test_preds, labels=["LOW", "MEDIUM", "HIGH"])
    report = classification_report(y_test, test_preds)

    print("=================== TEST SET EVALUATION ===================")
    print(f"Model Evaluated : {payload.get('model_name', 'Trained Classifier')}")
    print(f"Accuracy        : {acc * 100:.2f}%")
    print(f"Precision       : {prec:.4f}")
    print(f"Recall          : {rec:.4f}")
    print(f"F1-Score        : {f1:.4f}")
    print("\nConfusion Matrix (Rows: Actual [LOW, MEDIUM, HIGH], Cols: Predicted):")
    print(cm)
    print("\nDetailed Classification Report:")
    print(report)
    print("===========================================================")

    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "confusion_matrix": cm.tolist(),
        "report": report,
    }


if __name__ == "__main__":
    evaluate_saved_model()
