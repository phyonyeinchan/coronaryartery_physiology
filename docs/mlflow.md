# MLflow — Local dev and production notes

This document describes how to run MLflow for local development and how to configure a simple production deployment (backend store + artifact store).

## Quick local setup (development)

- Create a local `mlruns/` directory to store artifacts and add it to `.gitignore`:

```bash
mkdir -p mlruns
echo "mlruns/" >> .gitignore
```

- Run the MLflow UI locally (default, lightweight):

```bash
# start the UI on port 5000 and use a local sqlite file for the backend store
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

# open http://localhost:5000 in your browser
```

- Point your training script to that server (optional). Export the tracking URI in the same shell where you run training:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
# then run your training script normally, e.g.
python src/ml/train.py --data data/processed.csv --model models/model.pkl
```

Notes:
- The `mlflow ui` command above is intended for local development. It stores run metadata in `mlflow.db` (sqlite) and artifacts under `./mlruns`.
- For collaborative use, run a central MLflow server instead of the UI command.

## Minimal MLflow server (recommended for teams)

Use a database backend for tracking (Postgres/MySQL) and an object store (S3/GCS/Azure) for artifacts.

Example with PostgreSQL backend and S3 artifact root:

```bash
mlflow server \
  --backend-store-uri postgresql://USER:PASS@DB_HOST:5432/mlflow \
  --default-artifact-root s3://my-mlflow-artifacts/path \
  --host 0.0.0.0 --port 5000
```

Configuration notes:
- Ensure the service account/credentials used by MLflow have write access to the artifact store.
- Secure the MLflow server behind authentication (e.g., OAuth, reverse-proxy) and TLS in production.

## Using MLflow from code (training + inference)

- Automatic logging: MLflow supports automatic logging for many libraries (sklearn, xgboost, keras). See the MLflow docs.
- Manual logging example in Python:

```python
import mlflow

mlflow.set_experiment("cardio-risk-poc")
with mlflow.start_run():
    mlflow.log_param("model", "xgboost")
    mlflow.log_metric("auc", 0.87)
    mlflow.sklearn.log_model(model, "model")

# To point to a remote tracking server use MLFLOW_TRACKING_URI env var
```

## Local troubleshooting

- If `mlflow` commands are not found, install with `pip install mlflow` in your virtualenv.
- If UI shows no runs: confirm `MLFLOW_TRACKING_URI` in the shell where you started training, and confirm the `--default-artifact-root` path is writable.

## Security & operational checklist (brief)

- Use a managed DB for the backend store (Postgres) and an encrypted bucket for artifacts.
- Use TLS and an authenticated gateway (e.g., API gateway) in front of MLflow server.
- Rotate credentials for artifact store regularly and use least privilege.

## References

- MLflow docs: https://mlflow.org/docs/latest/
