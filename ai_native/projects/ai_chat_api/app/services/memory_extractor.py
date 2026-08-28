#                ChatService

#                      │

#          ┌───────────┴────────────┐

#          ▼                        ▼

# ConversationMemory        MemoryExtractor (LLM)
# Trình trích xuất bộ nhớ (LLM)
#          │                        │

#          ▼                        ▼

# Conversation History      Memory Candidates

#          │                        │

#          └──────────────┬─────────┘

#                         ▼

#                   MemoryStore

# Version 2:
#                     ChatService
#                           │
#         ┌─────────────────┼──────────────────┐
#         ▼                 ▼                  ▼
# ConversationMemory   MemoryStore     ContextBuilder
#         │                 ▲                   │
#         │                 │                   │
#         └────────▶ MemoryExtractor ◀─────────┘
#                           │
#                           ▼
#                     OllamaService
#                           │
#                           ▼

#   ChatService.chat()

#                            │
#                            ▼
#                 ConversationMemory.add(user)

#                            │
#                            ▼
#                 ContextBuilder.build()

#                            │
#                            ▼
#                   Ollama.generate()

#                            │
#                            ▼
#                  assistant_response

#                            │
#             ┌──────────────┴──────────────┐
#             ▼                             ▼
# ConversationMemory.add(assistant)    MemoryExtractor.extract_v2()

#                                             │
#                                             ▼
#                                       list[Memory]

#                                             │
#                                             ▼
#                                    MemoryStore.save()

#                                             │
#                                             ▼
#                                        PostgreSQL

#                            │
#                            ▼
#                  return assistant_response

# Conversation

#         │
#         ▼
# MemoryExtractor

#         │
#         ▼
# Extracted Memories

#         │
#         ▼
# MemoryScorer

#         │
#         ▼
# Scored Memories

#         │
#         ▼
# MemoryStore.save()

import json

from app.services.ollama_service import OllamaService
from app.schemas.memory_schema import MemoryList
from app.schemas.memory_candidate_schema import MemoryCandidate
from app.prompts.memory_prompt_eng import build_memory_prompt
from pydantic import ValidationError


class MemoryExtractor:
    def __init__(self, ollama_service: OllamaService):
        self.ollama_service = ollama_service

    def _build_conversation_v2(
        self,
        user_message: str,
        assistant_message: str,
    ) -> str:
        return f"User: {user_message}\nAssistant: {assistant_message}"

    def extract_v2(
        self, user_message: str, assistant_message: str
    ) -> list[MemoryCandidate]:
        conversation = self._build_conversation_v2(user_message, assistant_message)
        messages = [
            {
                "role": "system",
                "content": build_memory_prompt(),
            },
            {
                "role": "user",
                "content": f"""
                            Conversation:
        
                            {conversation}
        
                            Extract memories.
                            """,
            },
        ]

        memory_list = self.ollama_service.generate_structured(
            messages=messages,
            response_model=MemoryList,
        )

        return memory_list.memories
