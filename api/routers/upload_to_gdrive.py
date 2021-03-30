from api import tmp_path, mime, drive_id
from ..helpers.utils.utils import run_sync
from api import firebase, firebase_collection_user
from ..models.common import APIResponse

import shutil

from fastapi import APIRouter, File, UploadFile, Form


router = APIRouter(prefix="/api")


@router.post("/upload")
async def get_uploads(
    token: str = Form(...),
    device: str = Form(...),
    username: str = Form(...),
    file: UploadFile = File(...),
):
    user = firebase.get_user(username=username, collection=firebase_collection_user)

    if isinstance(user.to_dict(), dict):
        if token not in user.to_dict()["token"]:
            return APIResponse(status=404, message="USER_NOT_FOUND")
    else:
        return APIResponse(status=404, message="USER_NOT_FOUND")

    from ..helpers.gdrive.gdrive import GoogleDriveTools

    gdrive = GoogleDriveTools()

    cached_file = f"{tmp_path}{file.filename}"

    with open(cached_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    mime_type = mime.from_file(cached_file)

    await run_sync(
        gdrive.upload_file,
        cached_file=cached_file,
        file_name=file.filename,
        mime_type=mime_type,
        drive_id=drive_id,
        device=device,
    )

    return APIResponse(status=200, message="SUCCESS")
