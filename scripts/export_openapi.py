"""Dump the OpenAPI spec to openapi.json (a required deliverable).
Run from repo root:  python -m scripts.export_openapi
"""
import json

from app.main import app

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)

print("wrote openapi.json")
