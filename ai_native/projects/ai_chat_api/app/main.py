from fastapi import FastAPI
from app.routers.chat_router import router

app = FastAPI()
app.include_router(router)
