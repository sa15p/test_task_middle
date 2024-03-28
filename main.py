from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from route import router as tasks_router, outcomerouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(outcomerouter)
