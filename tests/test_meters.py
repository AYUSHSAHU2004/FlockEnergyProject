"""Tests mock the portal so they never hit the real site."""
from fastapi.testclient import TestClient

from app.main import app
from app.portal_client import portal

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_get_meter(monkeypatch):
    monkeypatch.setattr(portal, "get_meter", lambda mid: {"id": mid, "serial": "SN-1", "status": "active"})
    resp = client.get("/meters/M001")
    assert resp.status_code == 200
    assert resp.json()["serial_number"] == "SN-1"
