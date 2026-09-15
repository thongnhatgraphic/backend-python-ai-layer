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
# ----------------------------------------------------------------------
# User Message
#         │
#         ▼
# MemoryExtractor
#         │
#         ▼
# list[Memory]
#         │
#         ▼
# MemoryEvolution
#         │
#         ▼
# list[Memory]
#         │
#         ├──────────────┐
#         │              │
#         ▼              │
# if not memories        │
#         │              │
#         └──── return ──┘

#         ▼
# EmbeddingService.batch_embed()

#         ▼
# MemoryStore.save()

#         ▼
# PostgreSQL

from app.services.ollama_service import OllamaService
from app.services.conversation_memory import ConversationMemory
from app.services.context_builder import ContextBuilder
from app.services.memory_extractor import MemoryExtractor
from app.services.memory_store import MemoryStore
from app.services.memory_scorer import MemoryScorer
from app.services.memory_evolution import MemoryEvolution
from app.services.embedding_service import EmbeddingService
from app.services.rag_retriever import RagRetriever
from app.services.reranker_service import RerankerService
from app.services.releven_gate_service import RelevanceGate
from app.protocols.reranker import Reranker
from app.protocols.retriever import Retriever
from app.context.planner_context_history_selector import PlannerContextHistorySelector
from app.context.context_planner import ContextPlanner
from app.context.context_allocator import ContextAllocator

from app.schemas.memory_schema import Memory
from app.schemas.memory_candidate_schema import MemoryCandidate
from app.schemas.memory_score_schema import MemoryScore, MemoryScoreList
from app.schemas.memory_evolution_schema import (
    MemoryEvolutionOperation,
)

from app.context.context_priority import ContextImportance

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
        embedding_service: EmbeddingService,
        reranker_service: RerankerService,
        rag_retriever: Retriever,
        rag_reranker: Reranker,
        relevance_gate: RelevanceGate,
        ctx_history_selector: PlannerContextHistorySelector,
        context_planner: ContextPlanner,
        context_allocator: ContextAllocator,
    ):
        self.memory = memory
        self.llm = llm
        self.ctx = ctx
        self.memory_extractor = memory_extractor
        self.memory_store = memory_store
        self.memory_scorer = memory_scorer
        self.memory_evolution = memory_evolution
        self.embedding_service = embedding_service
        self.reranker_service = reranker_service
        self.rag_retriever = rag_retriever
        self.rag_reranker = rag_reranker
        self.relevance_gate = relevance_gate
        self.ctx_history_selector = ctx_history_selector
        self.context_planner = context_planner
        self.context_allocator = context_allocator

    def _filter_candidates(
        self,
        memories: list[MemoryCandidate],
        memory_scores: list[MemoryScore],
    ) -> list[MemoryCandidate]:

        if len(memories) != len(memory_scores):
            raise ValueError("Memory candidate count and score count must match")

        return [
            memory
            for memory, memory_score in zip(memories, memory_scores)
            if memory_score.score >= settings.MEMORY_SAVE_THRESHOLD
        ]

    def _materialize_memories(
        self,
        candidates: list[MemoryCandidate],
    ) -> list[Memory]:
        return [
            Memory(
                content=candidate.content,
                category=candidate.semantics.category,
                memory_key=candidate.semantics.memory_key,
                cardinality=candidate.semantics.cardinality,
                temporal_behavior=candidate.semantics.temporal_behavior,
            )
            for candidate in candidates
        ]

    def _embed_memories(
        self,
        memories: list[Memory],
    ) -> list[Memory]:

        if not memories:
            return []

        embeddings = self.embedding_service.batch_embed(
            memories=memories,
        )

        return [
            Memory(
                **memory.model_dump(exclude={"embedding"}),
                embedding=embedding,
            )
            for memory, embedding in zip(
                memories,
                embeddings,
            )
        ]

    def chat(self, user_id: UUID, message: str) -> str:
        # 1. Load previous conversation
        history = self.memory.get_history(user_id)

        # 2. Let the planner decide which context sources are useful
        context_plan = self.context_planner.plan(
            user_message=message,
            history=history,
        )

        print("\n===== CONTEXT PLAN =====")
        print(context_plan.model_dump())

        # 2.1 Check the importance level or priority of the Memory.
        memories = []
        if context_plan.memory.importance != ContextImportance.NONE:
            query_memory = self.embedding_service.embed(message)

            memories = self.memory_store.semantic_search(
                user_id=user_id,
                embedding=query_memory,
                limit=15,
            )

            memories = self.reranker_service.rerank(
                message,
                memories,
                limit=settings.MAX_RETRIEVAL_MEMORIES,
            )

        # 2.2 Check the importance level or priority of  the Rag_docs.
        rag_documents = []
        if context_plan.rag.importance != ContextImportance.NONE:
            rag_documents = self.rag_retriever.search(
                query=message,
                limit=settings.VECTOR_SEARCH_K,
            )
            print("\n===== RAG RETRIEVAL =====")
            print("retrieved:", len(rag_documents))

            rag_documents = self.rag_reranker.rerank(
                query=message,
                results=rag_documents,
            )

            rag_documents = rag_documents[: settings.RERANKER_LIMIT]
            print("\n===== RAG RERANKED =====")
            print("reranked:", len(rag_documents))
            before_gate = len(rag_documents)

            for document in rag_documents:
                print(
                    f"id={document.external_id} "
                    f"score={document.score:.4f} "
                    f"title={document.title}"
                )

            rag_documents = self.relevance_gate.filter(
                rag_documents,
            )
            print("\n===== RAG GATE =====")
            print("before:", before_gate)
            print("after:", len(rag_documents))

        # 3. Build candidates
        candidates = self.ctx.build_context_candidates(
            plan=context_plan,
            memories=memories,
            history=history,
            retrieved_documents=rag_documents,
        )

        # 4. Allocate global context budget
        allocation = self.context_allocator.allocate(
            budget=self.ctx.context_budget.max_input_tokens,
            candidates=candidates,
        )

        print("\n===== CONTEXT ALLOCATION =====")
        print("memory:", allocation.memory_tokens)
        print("rag:", allocation.rag_tokens)
        print("history:", allocation.history_tokens)
        print("total:", allocation.total_tokens)

        # 5. Build final context
        context = self.ctx.build(
            history,
            memories=memories,
            retrieved_documents=rag_documents,
            allocation=allocation,
            user_message=message,
        )
        # print("\n\n <--context--> \n\n", context)

        print("\n===== FINAL CONTEXT =====")

        for msg in context:
            print(f"[{msg['role']}]")
            print(msg["content"])
            print()

        # 3. Gọi LLM
        assistant_message = self.llm.generate(messages=context, format="text")

        # 4. Lưu message của user và assistant khi LLM trả lời thành công mới lưu
        # vào short-term memory
        self.memory.add_user_message(user_id, message)
        self.memory.add_assistant_message(user_id, assistant_message)

        print("\n\n ------------Start Extractor------------ \n\n")
        # 5. Extract long-term memory
        candidates = self.memory_extractor.extract_v2(message, assistant_message)
        # Cuộc hội thoại này có thể rút ra những memory nào?
        # print("\n\n 1. Extracted memory \n\n", candidates)

        # 5.1 Dựa vào user_message, assistant_message và memories
        # sử dụng memory_scorer để tìm kiếm memory trích xuất long-term
        memory_scores = self.memory_scorer.score(message, assistant_message, candidates)
        print("\n\n 5.1 memory_scores \n\n", memory_scores)

        filtered_memories = self._filter_candidates(candidates, memory_scores)
        print("\n\n 5.2 Filtered memories \n\n", filtered_memories)

        memories = self._materialize_memories(filtered_memories)
        print("\n\n 5.3 Materialized memories \n\n", memories)

        memories = self._embed_memories(memories)
        print("\n\n 5.4 Embedding memories after scores \n\n", memories)

        # 6 Sử dụng MemoryEvolution để quyết định memory long-term có struct ra sao
        evolution_results = self.memory_evolution.evolve(user_id, memories)
        print("\n\n 6 → Evolution \n\n", evolution_results)

        if evolution_results:
            insert_memories: list[Memory] = [
                result.memory
                for result in evolution_results
                if result.operation == MemoryEvolutionOperation.INSERT
            ]
            update_memories: list[Memory] = [
                result.memory
                for result in evolution_results
                if result.operation == MemoryEvolutionOperation.UPDATE
            ]

            if insert_memories:
                # 6.1 Sử dụng embedding model để tạo batch embeddings cho list memories
                embedded_memories = self.embedding_service.batch_embed(
                    memories=insert_memories
                )

                insert_memories = self._embed_memories(insert_memories)

                self.memory_store.save(user_id, insert_memories)

            if update_memories:
                # 6.2 Sử dụng embedding model để tạo batch embeddings cho list memories
                embedded_memories = self.embedding_service.batch_embed(
                    memories=update_memories
                )

                update_memories = self._embed_memories(update_memories)

                self.memory_store.update(user_id, update_memories)

        # 7. Phản hồi câu trả lời cho User
        return assistant_message
