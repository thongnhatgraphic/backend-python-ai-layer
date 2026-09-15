from sqlalchemy import text
from sqlmodel import Session, create_engine, bindparam

from app.core.settings import settings
from app.dependencies.ollama_dependency import client
from app.services.embedding_service import EmbeddingService

from pgvector.sqlalchemy import Vector

engine = create_engine(settings.DATABASE_URL)
embedding_service = EmbeddingService(client)


def explain_search_by_embedding(
    session: Session,
    query_embedding: list[float],
    limit: int,
):
    statement = text("""
        EXPLAIN (ANALYZE, BUFFERS)
        SELECT
            external_id,
            title,
            content,
            1 - (embedding <=> :query_embedding) AS score
        FROM rag_documents
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> :query_embedding
        LIMIT :limit
    """)

    statement = statement.bindparams(
        bindparam(
            "query_embedding",
            type_=Vector(768),
        ),
        bindparam("limit"),
    )

    statement = statement.bindparams(
        query_embedding=query_embedding,
        limit=limit,
    )

    return session.exec(statement).all()


QUERY = "0-dimensional biomaterials " "show inductive properties."

with Session(engine) as session:
    query_embedding = embedding_service.embed_text(QUERY)

    rows = explain_search_by_embedding(
        session=session,
        query_embedding=query_embedding,
        limit=10,
    )

    for row in rows:
        print(row[0])
