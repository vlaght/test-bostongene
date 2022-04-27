import hashlib
import logging

from celery import Celery
from sqlalchemy import create_engine

from cfg.rest import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, DATABASE_URLS
from core.exceptions import ObjectNotFound
from models.files import File, ProcessingStatus

celery = Celery(
    __name__,
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
)
logger = logging.getLogger(__name__)
engine = create_engine(DATABASE_URLS['main'])


def get_item_by_id(table, item_id):
    statement = table.select().where(
            table.c.id == item_id,
    )
    with engine.connect() as conn:
        res = conn.execute(statement)
    return res.fetchone()


def log_error(table, item_id, message):
    statement = table.update().where(
        table.c.id == item_id
    ).values(
        {
            'status': ProcessingStatus.failing,
            'log': message,
        }
    )
    with engine.connect() as conn:
        conn.execute(statement)


@celery.task(default_retry_delay=30, max_retries=3)
def calculate_md5(file_id):
    table = File.__table__
    try:
        item = get_item_by_id(table, file_id)
    except ObjectNotFound as exc:
        log_error(table, file_id, exc.args[0])
        return

    hasher = hashlib.md5()
    try:
        with open(item.path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
    except (IOError, SystemError) as exc:
        log_error(table, file_id, exc.args[0])
        raise exc

    values = {
        'md5': hasher.hexdigest(),
        'status': ProcessingStatus.success,
    }
    update_statement = table.update().where(
        table.c.id == file_id
    ).values(
        **values
    )
    with engine.connect() as conn:
        conn.execute(update_statement)
