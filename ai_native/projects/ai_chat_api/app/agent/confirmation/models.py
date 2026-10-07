from pydantic import BaseModel


class ConfirmationRequest(BaseModel):
    tool_call_id: str
    approved: bool
