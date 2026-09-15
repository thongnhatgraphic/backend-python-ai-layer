from app.services.context_builder import ContextBuilder

from app.services.token_counter import TokenCounter
from app.schemas.memory_rerank_schema import MemoryRerankResult
from app.schemas.retrieval_schema import RetrievalResult
from app.schemas.memory_schema import Memory

builder = ContextBuilder(
    token_counter=TokenCounter(),
    max_retrieved_context_tokens=3000,
    semantic_dedup_threshold=0.90,
)

memories = [
    MemoryRerankResult(
        memory=Memory(
            external_id="1",
            content="Content of memory 1",
            embedding=[1.0, 0.0, 0.0],
            category="learning",
            memory_key="focus",
            cardinality="single",
            temporal_behavior="current",
        ),
        score=1.0,
    ),
    MemoryRerankResult(
        memory=Memory(
            external_id="2",
            content="Content of memory 2",
            embedding=[0.99, 0.01, 0.0],
            category="learning",
            memory_key="focus",
            cardinality="single",
            temporal_behavior="current",
        ),
        score=0.95,
    ),
]

retrieved_documents = [
    RetrievalResult(
        external_id="1",
        score=1.0,
        title="Title document 1",
        content="Content of document 1",
    ),
    RetrievalResult(
        external_id="2",
        score=0.95,
        title="Title document 2",
        content="Content of document 2",
    ),
]

context = builder.build(
    history=[],
    memories=memories,
    retrieved_documents=retrieved_documents,
    user_message="What is ...?",
)

print(context)
