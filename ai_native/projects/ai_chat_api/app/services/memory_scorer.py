import json
from app.services.ollama_service import OllamaService
from app.schemas.memory_score_schema import MemoryScoreList, MemoryScore
from app.schemas.memory_schema import Memory
from app.schemas.memory_candidate_schema import MemoryCandidate
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
        memories: list[MemoryCandidate],
    ) -> str:
        # for index, score in enumerate(result.scores):
        #     candidate = memories[index]
        formatted = [
            {
                "candidate_index": index,
                "content": memory.content,
                "semantics": memory.semantics.model_dump(),
            }
            for index, memory in enumerate(memories)
        ]
        return json.dumps(formatted, ensure_ascii=False, indent=2)

    def _validate_scores(
        self,
        scores: MemoryScoreList,
        memories: list[MemoryCandidate],
    ) -> None:
        if len(scores.memories) != len(memories):
            raise ValueError(
                "Scorer must return exactly one score "
                "for each candidate. "
                f"Expected count={len(memories)}, "
                f"actual count={len(scores.memories)}"
            )

    def _score_candidate(
        self,
        conversation_format: str,
        candidate: MemoryCandidate,
    ) -> MemoryScore:

        prompt = build_memory_score_prompt(
            conversation_format=conversation_format,
            candidate_content=candidate.content,
            candidate_semantics=json.dumps(
                candidate.semantics.model_dump(),
                ensure_ascii=False,
                indent=2,
            ),
        )

        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]

        return self.ollama_service.generate_structured(
            messages=messages,
            response_model=MemoryScore,
        )

    def score(
        self,
        user_message: str,
        assistant_message: str,
        memories: list[MemoryCandidate],
    ) -> list[MemoryScore]:
        if not memories:
            return []

        formatted_memories = self._format_memories(memories)
        print("\n formatted_memories: \n", formatted_memories)

        conversation_format = self._build_conversation(
            user_message,
            assistant_message,
        )
        print("\n conversation_format: \n", conversation_format)

        scores: list[MemoryScore] = []

        for candidate in memories:
            score = self._score_candidate(
                conversation_format=conversation_format,
                candidate=candidate,
            )

            print("\n score: \n", score)
            scores.append(score)

        print("\n scores: \n", scores)

        return scores
