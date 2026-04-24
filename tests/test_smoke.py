import asyncio
from src.backend.app.main import health, InferRequest, infer


def test_health():
    res = asyncio.run(health())
    assert res == {"status": "ok"}


def test_infer_stub():
    req = InferRequest(patient_id="p1", features={"age": 70, "heart_rate": 90})
    res = asyncio.run(infer(req, user={"username": "dev", "roles": ["clinician"]}))
    assert "risk_score" in res
    assert 0.0 <= res["risk_score"] <= 1.0
