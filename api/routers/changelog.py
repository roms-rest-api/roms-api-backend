from api.helpers.commits.github import GithubSearcher
from fastapi import APIRouter, Form

from api import devices, telegraph, short_name, rom_pic
from api.models.common import APIResponse

router = APIRouter(prefix="/changelog")


@router.get("/device")
async def device_changelog(codename: str = Form(...)):
    codename = codename.lower()

    device = devices.get(codename)
    if not device:
        return APIResponse(status=404, message="DEVICE_NOT_FOUND")

    instance = GithubSearcher(codename)
    changelog = instance.get_changelog()
    response = telegraph.create_post(
        rom_name=short_name, device=codename, changelog=changelog, rom_pic=rom_pic
    )
    return changelog
