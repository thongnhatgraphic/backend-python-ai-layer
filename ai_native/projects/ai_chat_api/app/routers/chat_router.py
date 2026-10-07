from uuid import UUID, uuid4
from fastapi import APIRouter, Depends

from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse
from app.dependencies.ollama_dependency import get_ollama_service
from app.dependencies.context_builder_dependency import get_context_builder
from app.dependencies.conversation_memory_dependency import get_conversation_memory
from app.dependencies.memory_extractor_dependency import get_memory_extractor
from app.dependencies.memory_store_dependency import get_memory_store
from app.dependencies.memory_scorer_dependency import get_memory_scorer
from app.dependencies.memory_evolution_dependency import get_memory_evolution
from app.dependencies.reranker_dependency import get_reranker_dependency
from app.dependencies.embedding_dependency import get_embedding_dependency
from app.dependencies.rag_document_dependency import get_rag_retriever
from app.dependencies.rag_reranker_dependency import get_rag_reranker
from app.dependencies.relevance_gate_dependency import get_relevance_gate
from app.dependencies.context_history_dependency import (
    get_planner_context_history_selector,
)
from app.dependencies.context_planner_dependency import get_context_planner
from app.dependencies.context_allocator_dependency import get_context_allocator

from app.services.ollama_service import OllamaService
from app.services.context_builder import ContextBuilder
from app.services.conversation_memory import ConversationMemory
from app.services.chat_service import ChatService
from app.services.memory_extractor import MemoryExtractor
from app.services.memory_store import MemoryStore
from app.services.memory_scorer import MemoryScorer
from app.services.memory_evolution import MemoryEvolution
from app.services.embedding_service import EmbeddingService
from app.services.reranker_service import RerankerService
from app.services.rag_retriever import RagRetriever
from app.services.releven_gate_service import RelevanceGate
from app.context.context_planner import ContextPlanner
from app.context.planner_context_history_selector import PlannerContextHistorySelector
from app.context.context_allocator import ContextAllocator

from app.protocols.reranker import Reranker

router = APIRouter()


def get_chat_service(
    memory: ConversationMemory = Depends(get_conversation_memory),
    ollama: OllamaService = Depends(get_ollama_service),
    ctx: ContextBuilder = Depends(get_context_builder),
    memory_extractor: MemoryExtractor = Depends(get_memory_extractor),
    memory_store: MemoryStore = Depends(get_memory_store),
    memory_scorer: MemoryScorer = Depends(get_memory_scorer),
    memory_evolution: MemoryEvolution = Depends(get_memory_evolution),
    embedding_service: EmbeddingService = Depends(get_embedding_dependency),
    reranker_service: RerankerService = Depends(get_reranker_dependency),
    rag_retriever: RagRetriever = Depends(get_rag_retriever),
    rag_reranker: Reranker = Depends(get_rag_reranker),
    relevance_gate: RelevanceGate = Depends(get_relevance_gate),
    context_history_selector: PlannerContextHistorySelector = Depends(
        get_planner_context_history_selector
    ),
    context_planner: ContextPlanner = Depends(get_context_planner),
    context_allocator: ContextAllocator = Depends(get_context_allocator),
) -> ChatService:

    chat_service = ChatService(
        memory=memory,
        llm=ollama,
        ctx=ctx,
        memory_extractor=memory_extractor,
        memory_store=memory_store,
        memory_scorer=memory_scorer,
        memory_evolution=memory_evolution,
        embedding_service=embedding_service,
        reranker_service=reranker_service,
        rag_retriever=rag_retriever,
        rag_reranker=rag_reranker,
        relevance_gate=relevance_gate,
        ctx_history_selector=context_history_selector,
        context_planner=context_planner,
        context_allocator=context_allocator,
    )

    return chat_service


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest, llm_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    answer = llm_service.chat(
        UUID("43371a56-0d6b-454a-87c9-5c78b593122b"), request.message
    )

    return ChatResponse(answer=answer)
