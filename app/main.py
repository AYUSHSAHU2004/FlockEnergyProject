from fastapi import FastAPI

from app.routes import meters

app = FastAPI(
    title="Urja Meter API",
    version="0.1.0",
    description="Clean REST API over the legacy Urja Meter Ops portal.",
)

app.include_router(meters.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}

# Swagger UI is free at /docs, raw spec at /openapi.json
