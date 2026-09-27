import os
import csv
from typing import Dict, Any, List, Tuple
from .feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN


def load_split_data(
    file_path: str = "ML/risk_prediction/data/processed_data.csv",
) -> Tuple[List[List[float]], List[str], List[List[float]], List[str], List[List[float]], List[str]]:
    """
    Load and parse split dataset into X and y for train, validation, and test.
    """
    X_train, y_train = [], []
    X_val, y_val = [], []
    X_test, y_test = [], []

    with open(file_path, mode="r", encoding="utf-8") as f:
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
        from sklearn.metrics import accuracy_score, f1_score
        import joblib
    except ImportError as e:
        print(f"Warning: ML training libraries not installed: {e}")
        return {}

    X_train, y_train, X_val, y_val, X_test, y_test = load_split_data(data_path)

    print(f"Loaded {len(X_train)} train, {len(X_val)} validation, {len(X_test)} test samples.")

    # Model candidates
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
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
    payload = {
        "model_name": best_name,
        "model": best_model,
        "features": FEATURE_COLUMNS,
        "classes": list(best_model.classes_),
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
