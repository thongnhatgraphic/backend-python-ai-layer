from app.services.embedding_service import EmbeddingService
from app.services.rag_retriever import RagRetriever

from app.dependencies.ollama_dependency import client

from sqlmodel import Session, create_engine

from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL)

retriever = RagRetriever(
    embedding_service=EmbeddingService(client),
    engine=engine,
    ef_search=40,
)

results = retriever.search(
    query="0-dimensional biomaterials show inductive properties.",
    limit=20,
)

for rank, result in enumerate(results, start=1):
    print(
        rank,
        result.external_id,
        result.score,
        result.title,
    )
