from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.routers.__init__ import all_routers

# life cycle of app. Before app run fastAPI will be execute create_db first,
# and fastAPI will be execute shutdown_db or do something else before shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 START APP---------------------")

    # create_db()
    print("✅ Database created")
    print("✅ Redis connect ok")
    yield
    print("🛑 SHUTDOWN")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router["router"], tags=router["tags"])

