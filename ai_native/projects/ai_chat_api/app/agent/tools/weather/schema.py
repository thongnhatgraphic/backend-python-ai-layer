from pydantic import BaseModel, Field


class GetWeatherInput(BaseModel):
    city: str = Field(description="The city to get the weather for.")
