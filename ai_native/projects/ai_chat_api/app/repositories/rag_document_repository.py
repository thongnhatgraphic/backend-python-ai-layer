from sqlmodel import Session
from sqlalchemy import text, bindparam
from pgvector.sqlalchemy import Vector
from app.schemas.retrieval_schema import RetrievalResult


class RagDocumentRepository:

    def __init__(self, session: Session):
        self.session = session

    def search_by_embedding(
        self,
        query_embedding: list[float],
        limit: int,
        ef_search: int,
    ) -> list[RetrievalResult]:
        self.session.exec(text(f"SET LOCAL hnsw.ef_search = " f"{int(ef_search)}"))

        statement = text("""
            SELECT
                external_id,
                title,
                content,
                (1 - (embedding <=> :query_embedding)) AS score
            FROM rag_documents
            WHERE embedding IS NOT NULL
            ORDER BY (embedding <=> :query_embedding)
            LIMIT :limit
        """)

        statement = statement.bindparams(
            bindparam(
                "query_embedding",
                type_=Vector(768),
            ),
        )

        statement = statement.bindparams(
            query_embedding=query_embedding,
            limit=limit,
        )

        rows = self.session.exec(statement).all()

        return [
            RetrievalResult(
                external_id=row._mapping["external_id"],
                title=row._mapping["title"],
                content=row._mapping["content"],
                score=row._mapping["score"],
            )
            for row in rows
        ]
