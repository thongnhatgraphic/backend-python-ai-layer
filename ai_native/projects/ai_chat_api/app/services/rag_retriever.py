from app.schemas.retrieval_schema import RetrievalResult
from app.services.embedding_service import EmbeddingService

from app.repositories.rag_document_repository import RagDocumentRepository


class RagRetriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        rag_document_repository: RagDocumentRepository,
        ef_search: int = 40,
    ):
        self.embedding_service = embedding_service
        self.rag_document_repository = rag_document_repository
        self.ef_search = ef_search

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[RetrievalResult]:

        query_embedding = self.embedding_service.embed_text(query)

        return self.rag_document_repository.search_by_embedding(
            query_embedding=query_embedding,
            limit=limit,
            ef_search=self.ef_search,
        )
