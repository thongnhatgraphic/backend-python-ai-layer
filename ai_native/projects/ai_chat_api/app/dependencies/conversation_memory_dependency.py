from app.services.conversation_memory import ConversationMemory

memory = ConversationMemory()


def get_conversation_memory() -> ConversationMemory:
    return memory
