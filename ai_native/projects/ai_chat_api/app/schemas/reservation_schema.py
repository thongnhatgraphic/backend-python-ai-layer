from pydantic import BaseModel


class Reservation(BaseModel):
    acquired: bool
    owner_token: str | None = None
