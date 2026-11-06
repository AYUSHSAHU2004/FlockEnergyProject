"""Clean response shapes for YOUR API (not the portal's raw format)."""
from datetime import datetime

from pydantic import BaseModel


class Meter(BaseModel):
    id: str
    serial_number: str | None = None
    status: str | None = None
    feeder: str | None = None        # where it sits in the network
    transformer: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class Reading(BaseModel):
    timestamp: datetime
    kwh: float


class MeterList(BaseModel):
    items: list[Meter]
    page: int
    total: int | None = None
