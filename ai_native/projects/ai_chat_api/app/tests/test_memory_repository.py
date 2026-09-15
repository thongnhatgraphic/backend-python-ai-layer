import pytest
from uuid import uuid4
from sqlmodel import Session, text

from app.repositories.memory_repository import MemoryRepository
from app.schemas.memory_schema import Memory


def test_update_existing_memory(
    session: Session,
):
    repository = MemoryRepository(session)

    user_id = uuid4()
    memory_id = uuid4()

    memory = Memory(
        id=memory_id,
        content="User is learning Python.",
        embedding=[0.1] * 768,
    )

    repository.save(
        user_id,
        [memory],
    )

    check_statement = text("""
        SELECT id, user_id, content
        FROM memories
        WHERE id = :id
        AND user_id = :user_id
    """).bindparams(
        id=memory_id,
        user_id=user_id,
    )

    rows = session.exec(check_statement).all()

    assert len(rows) == 1

    updated_memory = Memory(
        id=memory_id,
        content="User is learning Java.",
        embedding=[0.2] * 768,
    )

    repository.update(
        user_id,
        [updated_memory],
    )

    statement = text("""
        SELECT id, content, embedding
        FROM memories
        WHERE id = :id
          AND user_id = :user_id
    """).bindparams(
        id=memory_id,
        user_id=user_id,
    )

    rows = session.exec(statement).all()

    assert len(rows) == 1

    row = rows[0]._mapping

    assert row["id"] == memory_id
    assert row["content"] == "User is learning Java."


def test_update_preserves_memory_id(
    session: Session,
):
    repository = MemoryRepository(session)

    user_id = uuid4()
    memory_id = uuid4()

    original = Memory(
        id=memory_id,
        content="User is learning Python.",
        embedding=[0.1] * 768,
    )

    repository.save(
        user_id,
        [original],
    )

    updated = Memory(
        id=memory_id,
        content="User is learning Java.",
        embedding=[0.2] * 768,
    )

    repository.update(
        user_id,
        [updated],
    )

    statement = text("""
        SELECT id
        FROM memories
        WHERE user_id = :user_id
    """).bindparams(
        user_id=user_id,
    )

    rows = session.exec(statement).all()

    assert len(rows) == 1
    assert rows[0]._mapping["id"] == memory_id


def test_update_does_not_cross_user_boundary(
    session: Session,
):
    repository = MemoryRepository(session)

    owner_user_id = uuid4()
    attacker_user_id = uuid4()

    memory_id = uuid4()

    original = Memory(
        id=memory_id,
        content="User is learning Python.",
        embedding=[0.1] * 768,
    )

    repository.save(
        owner_user_id,
        [original],
    )

    malicious_update = Memory(
        id=memory_id,
        content="User is learning Java.",
        embedding=[0.2] * 768,
    )

    repository.update(
        attacker_user_id,
        [malicious_update],
    )

    statement = text("""
        SELECT content
        FROM memories
        WHERE id = :id
          AND user_id = :user_id
    """).bindparams(
        id=memory_id,
        user_id=owner_user_id,
    )

    rows = session.exec(statement).all()

    assert len(rows) == 1

    content = rows[0]._mapping["content"]

    assert content == "User is learning Python."
