from pydantic import BaseModel, Field


class CreateTaskInput(BaseModel):
    title: str = Field(description="The task to create.")
