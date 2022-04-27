import logging
import os
import uuid
from typing import Optional

import aiofiles
from fastapi import APIRouter, HTTPException, Path, Query, UploadFile

from celery_app import calculate_md5
from cfg.rest import MEDIA_PATH
from core.files import FilesCore as core
from schemas.files import FileItemSchema, FilePageSchema

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/files", response_model=FileItemSchema)
async def create(file: UploadFile):
    logger.info('got file %s', file.filename)
    if not os.path.exists(MEDIA_PATH):
        os.mkdir(MEDIA_PATH)
    random_name = str(uuid.uuid4().hex)
    out_path = os.path.join(MEDIA_PATH, random_name)
    file_size = 0
    try:
        async with aiofiles.open(out_path, 'wb') as out_file:
            while content := await file.read(4096):
                await out_file.write(content)
                file_size += len(content)
    except (OSError, SystemError) as exc:
        logger.exception()
        raise HTTPException(
            status_code=500,
            detail=(
                'An error ({}) occured on the server side, '
                'contact the administrator'
            ).format(exc.args[0]),
        )
    values = {
        'name': file.filename,
        'path': out_path,
        'size': file_size,
    }
    item = await core.create(values)
    calculate_md5.delay(item.id)
    return item


@router.get("/files", response_model=FilePageSchema)
async def read_page(
    page: Optional[int] = Query(1, ge=1),
):
    page = await core.read_page(page=page)
    return page


@router.get("/files/{file_id}", response_model=FileItemSchema)
async def read(file_id: int = Path(..., ge=1)):
    item = await core.read(file_id)
    return item
