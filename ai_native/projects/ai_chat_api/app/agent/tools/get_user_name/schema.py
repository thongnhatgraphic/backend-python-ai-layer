from pydantic import BaseModel, Field


class GetUserNameInput(BaseModel):
    user_id: str = Field(description="The user ID to get the name for.")
