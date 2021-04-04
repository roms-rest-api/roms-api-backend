from api.helpers.commits.github import GithubSearcher
from fastapi import APIRouter, Form

from api import devices, firebase
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

    return changelog
