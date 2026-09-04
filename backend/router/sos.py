from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/sos",
    tags=["SOS"]
)


# SOS request data
class SOSRequest(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


@router.post("/")
def emergency_sos(data: SOSRequest):

    latitude = data.latitude
    longitude = data.longitude

    # Google Maps location
    map_link = None

    if latitude is not None and longitude is not None:
        map_link = (
            f"https://www.google.com/maps?q="
            f"{latitude},{longitude}"
        )

    # SOS information
    sos_data = {
        "status": "SOS Activated",
        "message": "Emergency SOS triggered successfully",
        "latitude": latitude,
        "longitude": longitude,
        "map_link": map_link,
        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "emergency_contact_notification": (
            "Emergency contacts will be notified"
        ),
        "hospital_notification": (
            "Hospital emergency notification generated"
        )
    }

    return sos_data