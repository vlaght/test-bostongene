
import datetime
import math
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import and_

from core.exceptions import ObjectNotFound
from core.helpers import check_existence, get_count
from models.database import database


class CrudFactory:
    PAGE_LIMIT = 25
    default_order_field = 'id'
    default_order_direction = 'desc'

    def __init__(self, table):
        self.table = table

    async def get_item_by_id(self, item_id: int):
        if not await check_existence(self.table, item_id):
            raise ObjectNotFound(self.table, item_id)
        statement = self.table.select().where(
                self.table.c.id == item_id,
        )
        return await database.fetch_one(statement)

    async def create(self, values: dict):
        statement = self.table.insert().returning(self.table)
        return await database.fetch_one(statement, values)

    async def read(self, item_id: int):
        return await self.get_item_by_id(item_id)

    async def update(self, item_id, values: dict):
        await check_existence(self.table, item_id)
        values['updated_dt'] = datetime.datetime.now()
        statement = self.table.update().where(
            self.table.c.id == item_id
        ).values(
            **values
        ).returning(
            self.table
        )
        return await database.fetch_one(
            statement,
            values,
        )

    async def delete(self, item_id: int):
        if not await check_existence(self.table, item_id):
            raise ObjectNotFound(self.table, item_id)

        statement = self.table.delete().where(
            self.table.c.id == item_id
        )
        await database.execute(statement)

    def _add_filters(self, statement, filters=None):
        _filters = []
        if filters:
            _filters.extend(filters)

        return statement.where(
            and_(*_filters)
        )

    def _add_orderings(self, statement, orderings: Optional[List] = None):
        default_order_field = getattr(self.table.c, self.default_order_field)
        default_order_field_with_direction = getattr(
            default_order_field,
            self.default_order_direction,
        )

        if not orderings:
            _orderings = [
                default_order_field_with_direction()
            ]
        elif orderings:
            _orderings = orderings

        return statement.order_by(
            *_orderings
        )

    def _construct_read_page_statement(self, filters, orderings):
        statement = self.table.select()
        statement = self._add_filters(statement, filters)
        statement = self._add_orderings(statement, orderings)
        return statement

    async def read_page(
        self,
        page=1,
        filters=None,
        orderings=None,
        limit=PAGE_LIMIT,
    ):
        if page < 1:
            page = 1
        statement = self._construct_read_page_statement(filters, orderings)
        total = await get_count(statement)
        last_page = max(1, math.ceil(total/limit))

        if page > last_page:
            raise HTTPException(404, detail='Page not found')

        statement = statement.offset(
            limit * (page-1)
        ).limit(
            limit
        )
        items = await database.fetch_all(statement)

        return dict(
            page=page,
            last_page=last_page,
            limit=limit,
            total=total,
            items=items,
        )
