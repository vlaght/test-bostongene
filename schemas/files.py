import datetime

from pydantic import BaseModel

from schemas.base import get_page_schema


class FileItemSchema(BaseModel):
    id: int
    name: str
    path: str
    size: int
    status: str
    created_dt: datetime.datetime
    updated_dt: datetime.datetime


class FilePageItemSchema(BaseModel):
    id: int
    name: str
    status: str
    md5: str = None
    updated_dt: datetime.datetime


FilePageSchema = get_page_schema(FilePageItemSchema)
