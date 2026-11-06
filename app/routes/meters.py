from fastapi import APIRouter, HTTPException, Query

from app.models import Meter, MeterList, Reading
from app.portal_client import PortalError, portal

router = APIRouter(prefix="/meters", tags=["meters"])


def to_meter(raw: dict) -> Meter:
    # TODO: map the portal's real field names -> clean names
    return Meter(
        id=str(raw.get("id")),
        serial_number=raw.get("serial"),
        status=raw.get("status"),
        feeder=raw.get("feeder"),
        transformer=raw.get("transformer"),
        latitude=raw.get("lat"),
        longitude=raw.get("lng"),
    )


@router.get("", response_model=MeterList)
def list_meters(page: int = Query(1, ge=1)):
    try:
        raw = portal.list_meters(page)
    except PortalError as e:
        raise HTTPException(502, str(e))
    return MeterList(items=[to_meter(m) for m in raw], page=page)


@router.get("/{meter_id}", response_model=Meter)
def get_meter(meter_id: str):
    try:
        return to_meter(portal.get_meter(meter_id))
    except PortalError as e:
        raise HTTPException(502, str(e))


@router.get("/{meter_id}/consumption", response_model=list[Reading])
def get_consumption(meter_id: str):
    try:
        raw = portal.get_consumption(meter_id)
    except PortalError as e:
        raise HTTPException(502, str(e))
    return [Reading(timestamp=r["ts"], kwh=r["kwh"]) for r in raw]  # TODO: real keys
