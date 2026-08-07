from fastapi import FastAPI
import asyncio

from contextlib import asynccontextmanager
from app.routers.__init__ import all_routers
from app.services.redis_listener import redis_listener


# life cycle of app. Before app run fastAPI will be execute create_db first,
# and fastAPI will be execute shutdown_db or do something else before shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 START APP---------------------")
    listener_task = asyncio.create_task(redis_listener())

    yield

    listener_task.cancel()
    print("🛑 SHUTDOWN")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router["router"], prefix=router["prefix"], tags=router["tags"])
