from fastapi import APIRouter

from api import devices, firebase
from api.models.frontend import DevicesResponse, DeviceBuildsResponse
from api.models.common import APIResponse

router = APIRouter(prefix="/frontend")


@router.get("/devices")
async def devices_handler():
    return DevicesResponse(status=200, message=devices.config)


@router.get("/builds/{device}/{version}")
async def builds_handler(device: str, version: str):
    if not devices.get(device):
        return APIResponse(status=404, message="DEVICE_NOT_FOUND")

    device_ref = firebase.get_builds_rldb().child(device).child(version)
    ref = device_ref.get()

    if not ref:
        return DeviceBuildsResponse(status=200, message=[])

    return DeviceBuildsResponse(status=200, message=[x[1] for x in list(ref.items())])
