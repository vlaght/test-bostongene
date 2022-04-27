import logging

from fastapi import FastAPI

from handlers import routers
from models.database import database, get_engine, metadata

logger = logging.getLogger(__name__)
app = FastAPI()

engine = get_engine()
metadata.create_all(bind=engine)

for r in routers:
    app.include_router(r)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
