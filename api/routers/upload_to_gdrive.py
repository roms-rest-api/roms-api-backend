from api import gdrive, tmp_path, mime, folder_id

import shutil

from loguru import logger
from fastapi import APIRouter, File, UploadFile


router = APIRouter(prefix="/api")


@router.post("/upload")
async def get_uploads(file: UploadFile = File(...)):
    cached_file = f"{tmp_path}{file.filename}"

    with open(cached_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    mime_type = mime.from_file(cached_file)

    logger.info(mime_type)

    uploaded_file = gdrive.upload_file(
        cached_file=cached_file,
        file_name=file.filename,
        mime_type=mime_type,
        folder_id=folder_id,
    )

    return uploaded_file
