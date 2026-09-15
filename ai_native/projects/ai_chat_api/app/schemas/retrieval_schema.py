from pydantic import BaseModel


class RetrievalResult(BaseModel):
    external_id: str
    score: float
    title: str
    content: str
