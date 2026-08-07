#                   User Message
#                       │
#                       ▼
#         ConversationMemory.get_history()
#                       │
#                       ▼
#         MemoryStore.search(user_message)
#             (Retrieval cho Chat)
#                       │
#                       ▼
#              ContextBuilder.build()
#                       │
#                       ▼
#                  LLM Chat
#                       │
#                       ▼
#         assistant_message được sinh ra
#                       │
#           ┌───────────┴────────────┐
#           ▼                        ▼
# ConversationMemory.add()    MemoryExtractor
#                                     │
#                                     ▼
#                           Canonical Memories
#                                     │
#                                     ▼
#                              MemoryScorer
#                                     │
#                                     ▼
#                           _filter_memories()
#                                     │
#                                     ▼
#                            MemoryEvolution
#                                     │
#                                     ▼
#                      MemoryStore.save()

from app.services.ollama_service import OllamaService
from app.services.conversation_memory import ConversationMemory
from app.services.context_builder import ContextBuilder
from app.services.memory_extractor import MemoryExtractor
from app.services.memory_store import MemoryStore
from app.services.memory_scorer import MemoryScorer
from app.services.memory_evolution import MemoryEvolution

# from app.services.embedding_service import EmbeddingService

from app.schemas.memory_schema import Memory
from app.schemas.memory_score_schema import MemoryScoreList
from app.core.settings import settings
from uuid import UUID, uuid4
import copy


class ChatService:

    def __init__(
        self,
        memory: ConversationMemory,
        llm: OllamaService,
        ctx: ContextBuilder,
        memory_extractor: MemoryExtractor,
        memory_store: MemoryStore,
        memory_scorer: MemoryScorer,
        memory_evolution: MemoryEvolution,
        # embedding_model: EmbeddingService,
    ):
        self.memory = memory
        self.llm = llm
        self.ctx = ctx
        self.memory_extractor = memory_extractor
        self.memory_store = memory_store
        self.memory_scorer = memory_scorer
        self.memory_evolution = memory_evolution
        # self.embedding_model = embedding_model

    def _filter_memories(
        self,
        memory_scores: MemoryScoreList,
    ) -> list[Memory]:
        return [
            Memory(content=item.content)
            for item in memory_scores.memories
            if item.score >= settings.MEMORY_SAVE_THRESHOLD
        ]

    def chat(self, user_id: UUID, message: str) -> str:
        # 1. Lấy lịch sử short-term trước đó
        history = self.memory.get_history(user_id)

        # 1.1 Lấy memory long-tern có lerevent với message trên
        memories = self.memory_store.search(
            user_id=user_id,
            query=message,
            limit=5,
        )

        # 2. Build context ( Ở đây lấy ra 20 message )
        context = self.ctx.build(history, memories=memories, user_message=message)

        # 3. Gọi LLM
        assistant_message = self.llm.generate(messages=context, format="text")

        # 4. Lưu message của user và assistant khi LLM trả lời thành công mới lưu
        # vào short-term memory
        self.memory.add_user_message(user_id, message)
        self.memory.add_assistant_message(user_id, assistant_message)
        print("\n\n Start Extractor \n\n")
        # 5. Extract long-term memory
        memories = self.memory_extractor.extract_v2(message, assistant_message)
        # Cuộc hội thoại này có thể rút ra những memory nào?
        print("\n\n memories \n\n", memories)

        # 5.1. Dựa vào user_message, assistant_message và memories
        # sử dụng memory_scorer để tìm kiếm memory trích xuất long-term
        memory_scores = self.memory_scorer.score(message, assistant_message, memories)
        print("\n\n memory_scores \n\n", memory_scores)

        filtered_memories = self._filter_memories(memory_scores)
        print("\n\n filtered_memories \n\n", filtered_memories)

        # 5.2 Sử dụng MemoryEvolution để quyết định memory long-term có struct ra sao
        final_memories = self.memory_evolution.evolve(user_id, filtered_memories)
        print("\n\n final_memories \n\n", final_memories)

        # 6. Sau khi có kiến thức của trích xuất long-term lưu dài hạn
        self.memory_store.save(user_id, filtered_memories)
        # 7. Phản hồi câu trả lời cho User
        return assistant_message
