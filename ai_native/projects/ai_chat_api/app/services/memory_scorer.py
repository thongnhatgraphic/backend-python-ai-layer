import json
from app.services.ollama_service import OllamaService
from app.schemas.memory_score_schema import MemoryScoreList
from app.schemas.memory_schema import Memory
from app.prompts.memory_score_prompt import build_memory_score_prompt


class MemoryScorer:
    def __init__(self, ollama_service: OllamaService):
        self.ollama_service = ollama_service

    def _build_conversation(
        self,
        user_message: str,
        assistant_message: str,
    ) -> str:
        return f"""
            User:
            {user_message}

            Assistant:
            {assistant_message}
        """.strip()

    def _format_memories(
        self,
        memories: list[Memory],
    ) -> str:
        return json.dumps(
            [memory.model_dump() for memory in memories], ensure_ascii=False, indent=2
        )

    def score(
        self,
        user_message: str,
        assistant_message: str,
        memories: list[Memory],
    ) -> MemoryScoreList:
        if not memories:
            return MemoryScoreList(memories=[])

        formatted_memories = self._format_memories(memories)
        conversation_format = self._build_conversation(user_message, assistant_message)

        prompt = build_memory_score_prompt(
            conversation_format=conversation_format,
            memories_extrator_format=formatted_memories,
        )
        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]

        memory_scores = self.ollama_service.generate_structured(
            messages=messages,
            response_model=MemoryScoreList,
        )

        print("\n\n\n memory_scores \n\n\n", memory_scores)

        return memory_scores
