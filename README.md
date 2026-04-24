Integrated Cardiology Risk Dashboard — scaffold

Overview
- PoC target: predict `in-hospital mortality` for cardiology cohort (INSPIRE -> MIMIC).
- FastAPI backend, XGBoost baseline, React frontend skeleton, DVC placeholders, MLflow tracking.

Quick start
1. Create venv and install:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run backend:
   ```bash
   uvicorn src.backend.app.main:app --reload --port 8000
   ```

3. Run tests:
   ```bash
   pytest -q
   ```

Data notes
- INSPIRE: open, recommended for initial PoC (CSV). See PhysioNet for download instructions.
- MIMIC-IV: credentialed (CITI + DUA). Apply via PhysioNet if you need larger sample.

DVC & data
- DVC pipeline stub present; run `dvc init` after adding large data and configure remote storage.
