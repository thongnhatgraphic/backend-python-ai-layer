from pydantic import BaseModel, Field


class CalculateSumInput(BaseModel):
    a: int = Field(description="The first number to add.")
    b: int = Field(description="The second number to add.")
