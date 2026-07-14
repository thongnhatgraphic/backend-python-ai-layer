from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "AI Chat API is running"}
