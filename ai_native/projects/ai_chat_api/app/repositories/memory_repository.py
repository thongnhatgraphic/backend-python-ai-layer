from sqlalchemy import text
from sqlmodel import Session
from uuid import UUID, uuid4
from app.schemas.memory_schema import Memory


class MemoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user_id: UUID, memories: list[Memory]):
        if not memories:
            return
        query = text("""
            INSERT INTO memories (
                id,
                user_id,
                content,
                created_at
            )
            VALUES (
                :id,
                :user_id,
                :content,
                CURRENT_TIMESTAMP
            )
        """)
        try:
            for memory in memories:
                self.session.exec(
                    query.bindparams(
                        id=uuid4(), user_id=user_id, content=memory.content
                    )
                )
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    def get(self, user_id: UUID) -> list[Memory]:
        query = text("""
            SELECT content
            FROM memories 
            WHERE user_id = :user_id
            ORDER BY created_at
        """)
        rows = self.session.exec(query, {"user_id": user_id}).all()
        if not rows:
            return []

        return [Memory(content=row._mapping["content"]) for row in rows]

    def search(self, user_id: UUID, query: str, limit: int = 5) -> list[Memory]:

        params = {"user_id": user_id}
        params["limit"] = limit
        if not query.strip():
            return []
        params["query"] = query
        statement = text("""
            SELECT
                id,
                user_id,
                content,
                created_at,
                ts_rank(
                    to_tsvector('simple', content),
                    plainto_tsquery('simple', :query)
                ) AS score
            FROM memories
            WHERE
                user_id = :user_id
                AND to_tsvector('simple', content)
                    @@ plainto_tsquery('simple', :query)
            ORDER BY score DESC
            LIMIT :limit
        """)

        rows = self.session.exec(statement.bindparams(**params)).all()

        if rows is None:
            return []

        return [Memory(content=row._mapping["content"]) for row in rows]

    def update(self, user_id: UUID, memories: list[Memory]):
        pass

    def delete(self, user_id: UUID):
        pass
