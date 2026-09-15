from sqlmodel import Session, text, bindparam, select
from app.database import get_session, engine
from app.schemas.memory_search_schema import MemorySearchResult
from app.schemas.memory_schema import Memory
from uuid import UUID
from app.repositories.memory_repository import MemoryRepository
from app.services.embedding_service import EmbeddingService
from ollama import Client
from pgvector.sqlalchemy import Vector
from app.models.memory_model import MemoryModel

repository = MemoryRepository(Session(engine))
embedding_client = Client(host="http://localhost:11434")
embedding_model = "nomic-embed-text"

experiment1 = "Tôi đang học Python"
experiment2 = "Python là ngôn ngữ tôi đang tập trung học"
experiment3 = "Tôi muốn mua một chiếc xe"


def backfill():
    embedding_service = EmbeddingService(embedding_client)

    with Session(engine) as session:
        memories = session.exec(
            select(MemoryModel).where(MemoryModel.embedding.is_(None))
        ).all()

        print(f"Found {len(memories)} memories")

        for memory in memories:
            embedded_memory = embedding_service.embed(Memory(content=memory.content))

            memory.embedding = embedded_memory.embedding

            print(f"Embedded: {memory.id} | " f"{memory.content[:50]}...")

        session.commit()

    print("Done!")


def embed(msg: str) -> list[float]:
    return embedding_client.embed(model=embedding_model, input=msg).embeddings[0]


def search(user_id: UUID):

    statement = text("""
            SELECT id, content
            FROM memories
            ORDER BY created_at;
        """)

    rows = repository.session.exec(statement).all()

    return [
        Memory(id=row._mapping["id"], content=row._mapping["content"]) for row in rows
    ]


# memories = search(user_id=UUID("43371a56-0d6b-454a-87c9-5c78b593122b"))
# for memory in memories:
#     print(memory.id, memory.content)


def semantic_search(
    user_id: UUID,
    embedding: list[float],
    limit: int = 10,
) -> list[MemorySearchResult]:

    params = {
        "user_id": user_id,
        "embedding": embedding,
        "limit": limit,
    }

    statement = text("""
        SELECT *,
               1 - (embedding <=> :embedding) AS score
        FROM memories
        WHERE user_id = :user_id
          AND embedding IS NOT NULL
        ORDER BY score DESC
        LIMIT :limit
    """)
    statement = statement.bindparams(
        bindparam("embedding", type_=Vector(768)),
    )

    rows = repository.session.exec(statement.bindparams(**params)).all()

    return [
        MemorySearchResult(
            memory=Memory(
                id=row._mapping["id"],
                content=row._mapping["content"],
            ),
            score=row._mapping["score"],
        )
        for row in rows
    ]


embedding1 = embed(experiment1)
embedding2 = embed(experiment2)
embedding3 = embed(experiment3)

# semantic_search1 = semantic_search(
#     UUID("43371a56-0d6b-454a-87c9-5c78b593122b"),
#     embedding1,
#     # threshold=0.5,
# )
# semantic_search2 = semantic_search(
#     UUID("43371a56-0d6b-454a-87c9-5c78b593122b"),
#     embedding2,
#     # threshold=0.5,
# )
# semantic_search3 = semantic_search(
#     UUID("43371a56-0d6b-454a-87c9-5c78b593122b"),
#     embedding3,
#     # threshold=0.5,
# )


# for result in semantic_search1:
#     print(result.memory.content, result.score)

# for result in semantic_search2:
#     print(result.memory.content, result.score)

# for result in semantic_search3:
#     print(result.memory.content, result.score)
