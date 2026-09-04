from fastapi import APIRouter

router = APIRouter(
    prefix="/sensor",
    tags=["Sensor"]
)

@router.get("/data")
def get_sensor_data():

    return {
        "heart_rate": 78,
        "spo2": 98,
        "latitude": 18.5204,
        "longitude": 73.8567,
        "speed": 32
    }