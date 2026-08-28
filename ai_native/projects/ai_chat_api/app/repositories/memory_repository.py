from sqlalchemy import text
from sqlmodel import Session, bindparam
from uuid import UUID, uuid4
from pgvector.sqlalchemy import Vector
import json

from app.schemas.memory_schema import Memory
from app.schemas.memory_search_schema import MemorySearchResult

# Postgresql thiết kế query embedding không phải theo cosine similarity.
# Nó thiết kế theo distance

# Ví dụ Cosine similarity =  1 => distance = 0 => lớn nhất gần nghĩa nhất
# Ví dụ Cosine similarity =  0.5 => distance = 0.5 => Hơi gần nghĩa :)))
# Ví dụ Cosine similarity =  0 => distance = 1 => Khác nghĩa luôn :D

# Vì vậy nó sort tăng dần theo distance: ORDER BY distance ASC

# Nguyên lý IVFFlat
# 1. Dùng K-Means tạo nhiều cluster.
# # 2. Mỗi cluster có một centroid.
# # 3. Query so sánh với tất cả centroid.
# # 4. Sắp xếp centroid theo distance.
# # 5. Mở 'probes' cluster gần nhất.
# # 6. Chỉ tính cosine với vector trong các cluster đó.
# # 7. Trả về Top K.
# CREATE INDEX memories_embedding_idx
# ON memories
# USING ivfflat (
#     embedding vector_cosine_ops
# )
# WITH (lists = 100);


# nguyên lý HNSW Hierarchical Navigable Small World
# Random Node
# ↓
# Neighbor Bạn của bạn
# ↓
# Neighbor Bạn của bạn của bạn
# ↓
# Neighbor Bạn của bạn của bạn và Bạn của bạn của bạn
# ↓
# Top K
# CREATE INDEX memories_embedding_idx
# ON memories
# USING hnsw (
#     embedding vector_cosine_ops
# );


class MemoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def _to_memory_search_result(self, row) -> MemorySearchResult:

        # embedding = row._mapping["embedding"]
        # print(type(embedding))
        # print(repr(embedding)[:20])
        # if isinstance(embedding, str):
        #     embedding = json.loads(embedding)

        return MemorySearchResult(
            memory=Memory(
                id=row._mapping["id"],
                content=row._mapping["content"],
                # embedding=embedding,
                category=row._mapping["category"],
                memory_key=row._mapping["memory_key"],
                cardinality=row._mapping["cardinality"],
                temporal_behavior=row._mapping["temporal_behavior"],
            ),
            score=row._mapping["score"],
        )

    def save(self, user_id: UUID, memories: list[Memory]):
        if not memories:
            return
        query = text("""
            INSERT INTO memories (
                id,
                user_id,
                content,
                embedding,
                category,
                memory_key,
                cardinality,
                temporal_behavior,
                created_at
            )
            VALUES (
                :id,
                :user_id,
                :content,
                :embedding,
                :category,
                :memory_key,
                :cardinality,
                :temporal_behavior,
                CURRENT_TIMESTAMP
            )
        """)
        try:
            for memory in memories:

                if memory.id is None:
                    raise ValueError("Memory id is required for save")

                self.session.exec(
                    query.bindparams(
                        id=memory.id,
                        user_id=user_id,
                        content=memory.content,
                        embedding=memory.embedding,
                        category=memory.category,
                        memory_key=memory.memory_key,
                        cardinality=memory.cardinality,
                        temporal_behavior=memory.temporal_behavior,
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

    def semantic_search(
        self, user_id: UUID, embedding: list[float], limit: int = 5
    ) -> list[MemorySearchResult]:
        params = {"user_id": user_id, "embedding": embedding, "limit": limit}
        statement = text("""
            SELECT *, (1 - (embedding <=> :embedding)) AS score
            FROM memories
            WHERE user_id = :user_id
            AND embedding IS NOT NULL
            ORDER BY score DESC
            LIMIT :limit
        """)

        statement = statement.bindparams(
            bindparam("embedding", type_=Vector(768)),
        )

        rows = self.session.exec(statement.bindparams(**params)).all()

        return [self._to_memory_search_result(row) for row in rows]

    def update(self, user_id: UUID, memories: list[Memory]):
        if not memories:
            return
        statement = text("""
            UPDATE memories
            SET
                content = :content,
                embedding = :embedding
            WHERE
                id = :id
                AND user_id = :user_id
        """)

        try:
            for memory in memories:
                if memory.id is None:
                    raise ValueError("Memory id is required for update")

                self.session.exec(
                    statement.bindparams(
                        id=memory.id,
                        user_id=user_id,
                        content=memory.content,
                        embedding=memory.embedding,
                    )
                )

            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def delete(self, user_id: UUID, memory_ids: list[UUID]):
        if not memory_ids:
            return

        statement = text("""
            DELETE FROM memories
            WHERE
                user_id = :user_id
                AND id = ANY(:memory_ids)
        """)
