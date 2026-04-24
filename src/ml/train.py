import argparse
import pandas as pd
import joblib
import os
import sys

# Ensure project root is on sys.path so `import src...` works when running scripts
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sklearn.model_selection import train_test_split
try:
    from xgboost import XGBClassifier
    _HAS_XGB = True
except Exception:
    _HAS_XGB = False
from src.ml.features import create_features
from sklearn.linear_model import LogisticRegression
try:
    import mlflow
    import mlflow.sklearn
    _HAS_MLFLOW = True
except Exception:
    _HAS_MLFLOW = False

def train(data_path: str, model_path: str):
    df = pd.read_csv(data_path)
    if "in_hospital_mortality" not in df.columns:
        raise ValueError("Expected column 'in_hospital_mortality' in data")
    X = create_features(df)
    y = df["in_hospital_mortality"].astype(int)
    # Only stratify if each class has at least 2 samples
    stratify_param = y if y.value_counts().min() >= 2 else None
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify_param
    )
    if _HAS_XGB:
        clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", n_estimators=50)
        clf.fit(X_train, y_train)
        model_type = "xgboost"
    else:
        # fallback to lightweight sklearn model when xgboost not available
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)
        model_type = "logistic_regression"

    os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)
    joblib.dump(clf, model_path)
    print(f"Saved model to {model_path}")

    # MLflow logging (optional)
    if _HAS_MLFLOW:
        try:
            with mlflow.start_run():
                mlflow.log_param("model_type", model_type)
                if model_type == "xgboost":
                    mlflow.log_param("n_estimators", 50)
                mlflow.sklearn.log_model(clf, "model")
                print("Logged model to MLflow")
        except Exception as e:
            print(f"MLflow logging failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="input CSV with features and in_hospital_mortality")
    parser.add_argument("--model", default="models/model.pkl", help="output model path")
    args = parser.parse_args()
    train(args.data, args.model)
