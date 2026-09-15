from uuid import UUID
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ConversationMemory:
    def __init__(self):
        self.messages_by_user: dict[UUID, list[dict[str, str]]] = {}

    def _ensure_history(
        self,
        user_id: UUID,
    ):
        if user_id not in self.messages_by_user:
            self.messages_by_user[user_id] = []

    # declare private function
    def _add_message(self, user_id: UUID, role: str, message: str):
        if not isinstance(message, str):
            raise TypeError(
                f"user message must be str, " f"got {type(message).__name__}"
            )

        self._ensure_history(user_id)

        self.messages_by_user[user_id].append({"role": role, "content": message})

    def get_history(self, user_id: UUID):

        self._ensure_history(user_id)

        return [message.copy() for message in self.messages_by_user[user_id]]

    def add_user_message(self, user_id: UUID, message: str):
        print(
            "\nADD USER MESSAGE:",
            repr(message),
            "TYPE:",
            type(message),
        )
        self._add_message(user_id, "user", message)

    def add_assistant_message(
        self,
        user_id: UUID,
        message: str,
    ):
        self._add_message(user_id, "assistant", message)
