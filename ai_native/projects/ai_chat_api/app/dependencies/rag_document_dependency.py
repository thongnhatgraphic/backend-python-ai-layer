from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.dependencies.embedding_dependency import get_embedding_dependency

from app.services.rag_retriever import RagRetriever
from app.services.embedding_service import EmbeddingService

from app.repositories.rag_document_repository import RagDocumentRepository
from app.core.settings import settings


def get_rag_retriever(
    session: Session = Depends(get_session),
    embedding_service: EmbeddingService = Depends(get_embedding_dependency),
) -> RagRetriever:

    repository = RagDocumentRepository(session=session)

    return RagRetriever(
        embedding_service=embedding_service,
        rag_document_repository=repository,
        ef_search=settings.RAG_HNSW_EF_SEARCH,
    )
