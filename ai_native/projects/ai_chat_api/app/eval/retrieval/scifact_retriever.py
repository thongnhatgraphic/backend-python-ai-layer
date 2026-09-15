from sqlalchemy import text
from sqlmodel import Session, create_engine, bindparam

from app.core.settings import settings
from app.dependencies.ollama_dependency import client
from app.services.embedding_service import EmbeddingService
from app.eval.schema.retrieval_schema import RetrievalResult

from pgvector.sqlalchemy import Vector

engine = create_engine(settings.DATABASE_URL)
embedding_service = EmbeddingService(client)


def search_by_embedding(
    session: Session,
    query_embedding: list[float],
    limit: int = 10,
    ef_search: int | None = None,
) -> list[RetrievalResult]:

    if ef_search is not None:
        tune_ef_search = text(f"SET LOCAL hnsw.ef_search = {int(ef_search)}")
        session.exec(tune_ef_search)

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

    rows = session.exec(statement).all()

    return [
        RetrievalResult(
            external_id=row._mapping["external_id"],
            title=row._mapping["title"],
            content=row._mapping["content"],
            score=row._mapping["score"],
        )
        for row in rows
    ]


def search(
    session: Session,
    query: str,
    limit: int = 10,
) -> list[RetrievalResult]:

    query_embedding = embedding_service.embed_text(query)

    return search_by_embedding(
        session=session,
        query_embedding=query_embedding,
        limit=limit,
    )
