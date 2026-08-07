from pydantic import BaseModel, RootModel


class Memory(BaseModel):
    content: str


class MemoryList(BaseModel):
    memories: list[Memory]
