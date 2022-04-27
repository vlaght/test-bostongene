from sqlalchemy import func

from models.database import database


async def get_count(statement):
    count_q = statement.with_only_columns([func.count()]).order_by(None)
    return await database.fetch_val(query=count_q)


async def check_existence(table, item_id: int):
    statement = table.select().where(
        table.c.id == item_id,
    )
    count = await get_count(statement)
    return count != 0
