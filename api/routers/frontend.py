from fastapi import APIRouter
from api import devices

from api.models.frontend import DevicesResponse

router = APIRouter(prefix="/frontend")


@router.get("/devices")
async def main_handler():
    return DevicesResponse(status=200, message=devices.config)
