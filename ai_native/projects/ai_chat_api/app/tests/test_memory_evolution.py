import pytest
from uuid import uuid4

from app.schemas.memory_schema import Memory
from app.schemas.memory_decision_schema import (
    MemoryAction,
    MemoryDecision,
)
from app.services.memory_evolution import MemoryEvolution


@pytest.fixture
def evolution():
    return MemoryEvolution(
        ollama_service=None,
        memory_store=None,
    )


@pytest.fixture
def candidates():
    return [
        Memory(content="User is learning Python."),
        Memory(content="User is learning AI and ML."),
    ]


def test_insert_valid(evolution, candidates):

    decision = MemoryDecision(
        action=MemoryAction.INSERT,
        candidate_index=None,
        resulting_content=None,
        reason="New information",
    )

    evolution._validate_decision(decision, candidates)


def test_insert_with_candidate_index_fails(evolution, candidates):

    decision = MemoryDecision(
        action=MemoryAction.INSERT,
        candidate_index=0,
        resulting_content=None,
        reason="New information",
    )

    with pytest.raises(ValueError):
        evolution._validate_decision(decision, candidates)


def test_insert_with_resulting_content_none(evolution, candidates):
    decision = MemoryDecision(
        action=MemoryAction.INSERT,
        candidate_index=None,
        resulting_content="Content new information",
        reason="New information",
    )
    with pytest.raises(ValueError):
        evolution._validate_decision(decision, candidates)


def test_duplicate_valid(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.DUPLICATE,
        candidate_index=0,
        resulting_content=None,
        reason="Same semantic meaning",
    )

    evolution._validate_decision(
        decision,
        candidates,
    )


def test_duplicate_without_candidate_fails(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.DUPLICATE,
        candidate_index=None,
        resulting_content=None,
        reason="Duplicate",
    )

    with pytest.raises(ValueError):
        evolution._validate_decision(
            decision,
            candidates,
        )


def test_update_valid(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.UPDATE,
        candidate_index=0,
        resulting_content="User is currently learning Java.",
        reason="New information replaces old focus",
    )

    evolution._validate_decision(
        decision,
        candidates,
    )


def test_update_without_resulting_content_fails(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.UPDATE,
        candidate_index=0,
        resulting_content=None,
        reason="Update old memory",
    )

    with pytest.raises(ValueError):
        evolution._validate_decision(
            decision,
            candidates,
        )


def test_update_invalid_candidate_index_fails(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.UPDATE,
        candidate_index=99,
        resulting_content="User is learning Java.",
        reason="Update",
    )

    with pytest.raises(ValueError):
        evolution._validate_decision(
            decision,
            candidates,
        )


def test_merge_valid(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.MERGE,
        candidate_index=0,
        resulting_content=("User is learning Python, AI and ML."),
        reason="New information complements existing memory",
    )

    evolution._validate_decision(
        decision,
        candidates,
    )


def test_merge_without_resulting_content_fails(
    evolution,
    candidates,
):
    decision = MemoryDecision(
        action=MemoryAction.MERGE,
        candidate_index=0,
        resulting_content=None,
        reason="Merge",
    )

    with pytest.raises(ValueError):
        evolution._validate_decision(
            decision,
            candidates,
        )


def test_execute_insert(evolution, candidates):
    memory = Memory(content="User is learning Java.")

    decision = MemoryDecision(
        action=MemoryAction.INSERT,
        reason="New information",
    )

    result = evolution._execute(
        memory,
        candidates,
        decision,
    )

    assert result.memory is memory


def test_execute_duplicate(evolution, candidates):
    memory = Memory(content="User is learning Python.")

    decision = MemoryDecision(
        action=MemoryAction.DUPLICATE,
        candidate_index=0,
        reason="Same semantic meaning",
    )

    result = evolution._execute(
        memory,
        candidates,
        decision,
    )

    assert result.memory is None


def test_execute_update(evolution, candidates):
    memory = Memory(content="User is now focusing on Java.")

    decision = MemoryDecision(
        action=MemoryAction.UPDATE,
        candidate_index=0,
        resulting_content=("User is now focusing on Java."),
        reason="The new focus replaces Python.",
    )

    result = evolution._execute(
        memory,
        candidates,
        decision,
    )

    assert result is not None
    assert result.memory.id == candidates[0].id
    assert result.memory.content == ("User is now focusing on Java.")


def test_execute_merge(evolution, candidates):
    memory = Memory(content="User is learning AI and ML.")

    decision = MemoryDecision(
        action=MemoryAction.MERGE,
        candidate_index=0,
        resulting_content=("User is learning Python, AI and ML."),
        reason=("The new information complements " "the existing memory."),
    )

    result = evolution._execute(
        memory,
        candidates,
        decision,
    )

    assert result.memory is not None
    assert result.memory.id == candidates[0].id
    assert result.memory.content == ("User is learning Python, AI and ML.")


def test_update_keeps_existing_memory_id(
    evolution,
    candidates,
):
    new_memory = Memory(
        content="User is learning Java.",
        id=uuid4(),
    )

    decision = MemoryDecision(
        action=MemoryAction.UPDATE,
        candidate_index=1,
        resulting_content=("User is currently learning Java."),
        reason="Updated information",
    )

    result = evolution._execute(
        new_memory,
        candidates,
        decision,
    )

    assert result.memory is not None

    # UPDATE must preserve existing memory identity.
    assert result.memory.id == candidates[1].id

    # UPDATE must use the new resulting content.
    assert result.memory.content == ("User is currently learning Java.")

    # UPDATE must not reuse the new memory's identity.
    assert result.memory.id != new_memory.id
