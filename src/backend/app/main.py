from fastapi import FastAPI, Depends, HTTPException, Header, Request
from typing import Optional
from pydantic import BaseModel
from src.backend.app.auth import get_current_user
import joblib
import os
import pandas as pd

app = FastAPI(title="Cardio Risk Dashboard API")
from fastapi.middleware.cors import CORSMiddleware

# ... (app = FastAPI() အောက်နားမှာ ထည့်ရန်)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # အားလုံးကို ခွင့်ပြုလိုက်တာပါ
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Try to load a trained model if available
MODEL = None
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', 'models', 'model.pkl')
MODEL_PATH = os.path.abspath(MODEL_PATH)
if os.path.exists(MODEL_PATH):
    try:
        MODEL = joblib.load(MODEL_PATH)
        print(f"Loaded model from {MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load model: {e}")


class InferRequest(BaseModel):
    patient_id: str
    features: dict


class InferResponse(BaseModel):
    patient_id: str
    risk_score: float
    explanation: dict = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/infer", response_model=InferResponse)
async def infer(req: InferRequest, user=Depends(get_current_user)):
    # Backward-compatible placeholder inference
    features = req.features
    age = float(features.get("age", 60))
    hr = float(features.get("heart_rate", 80))
    risk = 1 / (1 + (2.71828 ** (-(0.02*(age-60) + 0.01*(hr-80)))))
    explanation = {"drivers": {"age": 0.02*(age-60), "heart_rate": 0.01*(hr-80)}}
    return {"patient_id": req.patient_id, "risk_score": float(risk), "explanation": explanation}


@app.post("/predict", response_model=InferResponse)
async def predict(req: InferRequest, user=Depends(get_current_user)):
    """Use the trained model stored at `models/model.pkl` to produce a risk score.
    Returns 503 if no model is loaded.
    """
    global MODEL
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not available")
    # Convert features dict to single-row DataFrame matching training feature pipeline
    df = pd.DataFrame([req.features])
    # Basic preprocessing: ensure numeric types
    df = df.select_dtypes(include=["number"]).fillna(0)
    # If model recorded training feature names, reindex to that order and fill missing with 0
    try:
        feature_names = getattr(MODEL, "feature_names_in_", None)
        if feature_names is not None:
            # ensure DataFrame has all expected columns in the same order
            df = df.reindex(columns=list(feature_names), fill_value=0)
    except Exception:
        pass
    # If model has predict_proba, use positive class probability
    try:
        proba = MODEL.predict_proba(df)
        risk = float(proba[0][1]) if proba.shape[1] > 1 else float(proba[0][0])
    except Exception:
        pred = MODEL.predict(df)
        risk = float(pred[0])
    return {"patient_id": req.patient_id, "risk_score": risk, "explanation": {}}


@app.post("/reload-model")
async def reload_model(request: Request, x_reload_token: Optional[str] = Header(default=None), user=Depends(get_current_user)):
    """Reload the model from disk.

    Security: either the `X-Reload-Token` header must match the environment
    `RELOAD_SECRET`, or the authenticated `user` must have an admin role
    (one of `admin`, `mlops`). If `RELOAD_SECRET` is not set, only role-based
    access is enforced.
    """
    import logging
    import os
    global MODEL

    logger = logging.getLogger("reload_model")
    env_secret = os.environ.get("RELOAD_SECRET", "")

    # Check header token first (if provided)
    if env_secret:
        if not x_reload_token:
            logger.warning("Reload attempt without token from %s", request.client.host if request.client else "unknown")
            raise HTTPException(status_code=401, detail="Missing reload token")
        if x_reload_token != env_secret:
            logger.warning("Invalid reload token attempt from %s", request.client.host if request.client else "unknown")
            raise HTTPException(status_code=403, detail="Forbidden")

    # Role-based fallback/requirement: user must have admin-like role
    allowed_roles = {"admin", "mlops"}
    user_roles = set(user.get("roles", [])) if isinstance(user, dict) else set()
    if not (env_secret and x_reload_token == env_secret) and not (user_roles & allowed_roles):
        logger.warning("Unauthorized reload attempt by user=%s roles=%s", user.get("username") if isinstance(user, dict) else str(user), user_roles)
        raise HTTPException(status_code=403, detail="Forbidden")

    if not os.path.exists(MODEL_PATH):
        logger.error("Model file not found at %s", MODEL_PATH)
        raise HTTPException(status_code=404, detail="Model file not found")
    try:
        MODEL = joblib.load(MODEL_PATH)
        logger.info("Model reloaded from %s by user=%s", MODEL_PATH, user.get("username") if isinstance(user, dict) else str(user))
        return {"status": "reloaded", "path": MODEL_PATH}
    except Exception as e:
        logger.exception("Reload failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Reload failed: {e}")
@app.get("/")
def read_root():
    return {"message": "Welcome to Coronary Artery Physiology API"}
@app.get("/")
def read_root():
    return {"message": "Welcome to Coronary Artery Physiology API"}
