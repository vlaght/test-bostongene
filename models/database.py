import os

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from cfg.rest import DATABASE_URLS

Base = declarative_base()
metadata = Base.metadata


def get_db(target: str = 'main'):
    return databases.Database(DATABASE_URLS[target])


def get_engine(target: str = 'main'):
    return create_engine(DATABASE_URLS[target])


database = get_db('test') if os.getenv('TESTING') else get_db()
