import asyncio
import pytest
from types import SimpleNamespace
from fastapi import HTTPException

from src.backend.app.main import reload_model


def make_request(host: str = "testhost"):
    return SimpleNamespace(client=SimpleNamespace(host=host))


def test_reload_with_token(monkeypatch):
    monkeypatch.setenv("RELOAD_SECRET", "testtoken")
    req = make_request()
    res = asyncio.run(reload_model(req, x_reload_token="testtoken", user={"username": "dev", "roles": ["clinician"]}))
    assert res.get("status") == "reloaded"


def test_reload_with_admin_role(monkeypatch):
    monkeypatch.delenv("RELOAD_SECRET", raising=False)
    req = make_request()
    res = asyncio.run(reload_model(req, x_reload_token=None, user={"username": "admin", "roles": ["admin"]}))
    assert res.get("status") == "reloaded"


def test_reload_missing_token(monkeypatch):
    monkeypatch.setenv("RELOAD_SECRET", "testtoken2")
    req = make_request()
    with pytest.raises(HTTPException) as ei:
        asyncio.run(reload_model(req, x_reload_token=None, user={"username": "dev", "roles": ["clinician"]}))
    assert ei.value.status_code == 401


def test_reload_invalid_token(monkeypatch):
    monkeypatch.setenv("RELOAD_SECRET", "testtoken3")
    req = make_request()
    with pytest.raises(HTTPException) as ei:
        asyncio.run(reload_model(req, x_reload_token="wrong", user={"username": "dev", "roles": ["clinician"]}))
    assert ei.value.status_code == 403
