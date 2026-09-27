import os
import csv
from typing import Dict, Any, List, Tuple

try:
    from .feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
except ImportError:
    try:
        from ML.risk_prediction.feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
    except ImportError:
        from feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN


def _find_data_path(default_path: str) -> str:
    if os.path.exists(default_path):
        return default_path
    local_path = os.path.join(os.path.dirname(__file__), "data", "processed_data.csv")
    if os.path.exists(local_path):
        return local_path
    return default_path


def load_split_data(
    file_path: str = "ML/risk_prediction/data/processed_data.csv",
) -> Tuple[List[List[float]], List[str], List[List[float]], List[str], List[List[float]], List[str]]:
    """
    Load and parse split dataset into X and y for train, validation, and test.
    """
    X_train, y_train = [], []
    X_val, y_val = [], []
    X_test, y_test = [], []

    resolved_path = _find_data_path(file_path)
    with open(resolved_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            split = row.get("dataset_split", "train").lower()
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            target = row[TARGET_COLUMN].strip().upper()

            if split == "train":
                X_train.append(features)
                y_train.append(target)
            elif split == "validation":
                X_val.append(features)
                y_val.append(target)
            elif split == "test":
                X_test.append(features)
                y_test.append(target)

    return X_train, y_train, X_val, y_val, X_test, y_test


def train_and_save_model(
    data_path: str = "ML/risk_prediction/data/processed_data.csv",
    model_output_path: str = "ML/risk_prediction/model.pkl",
) -> Dict[str, Any]:
    """
    Train baseline models (Logistic Regression, Decision Tree, Random Forest)
    using scikit-learn / joblib, evaluate, and serialize the best model.
    """
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.metrics import accuracy_score, f1_score
        import joblib
    except ImportError as e:
        print(f"Warning: ML training libraries not installed: {e}")
        return {}

    X_train_raw, y_train, X_val_raw, y_val, X_test_raw, y_test = load_split_data(data_path)

    try:
        import pandas as pd
        X_train = pd.DataFrame(X_train_raw, columns=FEATURE_COLUMNS)
        X_val = pd.DataFrame(X_val_raw, columns=FEATURE_COLUMNS)
        X_test = pd.DataFrame(X_test_raw, columns=FEATURE_COLUMNS)
    except Exception:
        X_train, X_val, X_test = X_train_raw, X_val_raw, X_test_raw

    print(f"Loaded {len(X_train)} train, {len(X_val)} validation, {len(X_test)} test samples.")

    # Model candidates
    models = {
        "LogisticRegression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42)),
        "DecisionTree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
    }

    best_name = None
    best_model = None
    best_score = -1.0
    val_results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        val_preds = model.predict(X_val)
        acc = accuracy_score(y_val, val_preds)
        f1 = f1_score(y_val, val_preds, average="weighted")
        val_results[name] = {"accuracy": acc, "f1": f1}
        print(f"Model {name} -> Val Accuracy: {acc:.4f}, Val F1: {f1:.4f}")

        if f1 > best_score:
            best_score = f1
            best_name = name
            best_model = model

    print(f"\nBest Model: {best_name} (F1: {best_score:.4f})")

    # Serialize best model
    classes_list = list(getattr(best_model, "classes_", getattr(getattr(best_model, "steps", [("", None)])[-1][1], "classes_", ["LOW", "MEDIUM", "HIGH"])))
    payload = {
        "model_name": best_name,
        "model": best_model,
        "features": FEATURE_COLUMNS,
        "classes": classes_list,
    }
    joblib.dump(payload, model_output_path)
    print(f"Saved best model artifact to: {model_output_path}")

    return {
        "best_model": best_name,
        "validation_results": val_results,
        "model_path": model_output_path,
    }


if __name__ == "__main__":
    train_and_save_model()
