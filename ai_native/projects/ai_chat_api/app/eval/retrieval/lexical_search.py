from sqlmodel import Session, text, bindparam, create_engine
from app.eval.schema.retrieval_schema import RetrievalResult

from app.core.settings import settings
from app.services.embedding_service import EmbeddingService
from app.dependencies.ollama_dependency import client

engine = create_engine(settings.DATABASE_URL)
embedding_service = EmbeddingService(client)


def lexical_search(
    session: Session,
    query: str,
    limit: int = 20,
):

    statement = text("""
        SELECT
            external_id,
            title,
            content,
            ts_rank_cd(
                to_tsvector(
                    'english',
                    coalesce(title, '') || ' ' || content
                ),
                plainto_tsquery('english', :query)
            ) AS score
        FROM rag_documents
        WHERE to_tsvector(
            'english',
            coalesce(title, '') || ' ' || content
        )
        @@ plainto_tsquery('english', :query)
        ORDER BY score DESC
        LIMIT :limit
    """)

    statement = statement.bindparams(
        bindparam("query"),
        bindparam("limit"),
    )

    rows = session.exec(
        statement,
        params={
            "query": query,
            "limit": limit,
        },
    ).all()

    return [
        RetrievalResult(
            external_id=row._mapping["external_id"],
            title=row._mapping["title"],
            content=row._mapping["content"],
            score=row._mapping["score"],
        )
        for row in rows
    ]


def main():
    with Session(engine) as session:
        query = "1 in 5 million in UK have abnormal PrP positivity."

        result = lexical_search(session=session, query=query, limit=20)

        print("result", result)


main()
