from fastapi import HTTPException
from sqlalchemy import Table


class ObjectNotFound(HTTPException):

    def __init__(self, table: Table, item_id: int):
        super().__init__(
            404,
            detail='{}<id:{}> Not found'.format(
                table,
                item_id,
            )
        )
