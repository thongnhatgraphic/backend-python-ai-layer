from sqlmodel import Session, create_engine, select

from app.models.memory_model import MemoryModel
from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL)


def classify_memory(memory: MemoryModel) -> dict:
    content = memory.content.lower()

    if "user's name" in content or "tên của user" in content:
        return {
            "category": "identity",
            "memory_key": "name",
            "cardinality": "single",
            "temporal_behavior": "current",
        }

    if "nickname" in content or "ngọt" in content:
        return {
            "category": "identity",
            "memory_key": "nickname",
            "cardinality": "single",
            "temporal_behavior": "current",
        }

    if "learning python" in content:
        return {
            "category": "learning",
            "memory_key": "focus",
            "cardinality": "single",
            "temporal_behavior": "current",
        }

    if "roadmap" in content and "java developer" in content:
        return {
            "category": "career",
            "memory_key": "goal",
            "cardinality": "single",
            "temporal_behavior": "current",
        }

    if "billiards" in content:
        return {
            "category": "interest",
            "memory_key": "hobby",
            "cardinality": "multiple",
            "temporal_behavior": "current",
        }

    raise ValueError(f"Cannot classify memory id={memory.id}: " f"{memory.content}")


def main():
    with Session(engine) as session:
        memories = session.exec(select(MemoryModel)).all()

        for memory in memories:
            semantics = classify_memory(memory)

            memory.category = semantics["category"]
            memory.memory_key = semantics["memory_key"]
            memory.cardinality = semantics["cardinality"]
            memory.temporal_behavior = semantics["temporal_behavior"]

            print(
                memory.id,
                memory.content,
                semantics,
            )

        session.commit()


if __name__ == "__main__":
    main()
