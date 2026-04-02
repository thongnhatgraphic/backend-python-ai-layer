from fastapi import FastAPI

from app.database import create_db
from contextlib import asynccontextmanager
from app.routers.__init__ import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 START APP---------------------")

    create_db()
    print("✅ Database created")

    yield

    print("🛑 SHUTDOWN")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router["router"], tags=router["tags"])

