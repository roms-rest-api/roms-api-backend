from fastapi import APIRouter

from api import devices, firebase
from api.models.frontend import DevicesResponse, DeviceBuildsResponse
from api.models.common import APIResponse

router = APIRouter(prefix="/frontend")


@router.get("/devices")
async def devices_handler():
    return DevicesResponse(status=200, message=list(devices.config.values()))


@router.get("/builds/{device}/{version}")
async def builds_handler(device: str, version: str):
    if not devices.get(device):
        return APIResponse(status=404, message="DEVICE_NOT_FOUND")

    device_ref = firebase.get_builds_rldb().child(device).child(version)
    ref = device_ref.get()

    if not ref:
        return DeviceBuildsResponse(status=200, message=[])

    result = []
    for item in ref.items():
        dict_obj = item[1]
        dict_obj['id'] = item[0]

        result.append(dict_obj)

    return DeviceBuildsResponse(status=200, message=list(ref.values()))
