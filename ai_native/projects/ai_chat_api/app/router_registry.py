from fastapi import FastAPI
from app.routers.chat_router import router as chat_router
from app.routers.agent import router as agent_router

# app = FastAPI()
# from starlette.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

all_router = [
    {
        "router": chat_router,
        "prefix": "/chat",
        "tags": ["Chats"],
    },
    {
        "router": agent_router,
        "prefix": "/agent",
        "tags": ["Agents"],
    },
]
