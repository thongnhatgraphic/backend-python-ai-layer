import pytest

from uuid import uuid4
from app.services.memory_evolution import MemoryEvolution
from app.schemas.memory_decision_schema import MemoryDecision, MemoryAction
from app.schemas.memory_schema import Memory


@pytest.fixture
def memory_evolution():
    return MemoryEvolution(ollama_service=None, memory_store=None)


def test_case_update(memory_evolution):
    candidates_database = [
        Memory(
            id=uuid4(),
            category="learning",
            memory_key="forcus",
            content="learning Python",
            embedding=[0.1, 0.2, 0.3],
            cardinality="single",
            temporal_behavior="current",
        ),
        Memory(
            id=uuid4(),
            category="interest",
            memory_key="project",
            content="User is interested in creating a wooden toy car model",
            embedding=[0.1, 0.2, 0.3],
            cardinality="single",
            temporal_behavior="current",
        ),
    ]
    memory_from_extractor = Memory(
        id=None,
        category="learning",
        memory_key="forcus",
        content="User is forcus on learning Java",
        embedding=[0.3, 0.2, 0.3],
        cardinality="single",
        temporal_behavior="current",
    )
    memory_semantic_match = memory_evolution._find_semantic_slot_match(
        memory_from_extractor,
        candidates_database,
    )
    assert memory_semantic_match is not None
    assert memory_semantic_match.content == candidates_database[0].content
    assert memory_semantic_match.id == candidates_database[0].id


def test_find_semantic_slot_match_returns_none_for_different_key(
    memory_evolution,
):
    candidates = [
        Memory(
            id=uuid4(),
            category="learning",
            memory_key="focus",
            content="User is currently focused on learning Python.",
            embedding=[0.1, 0.2, 0.3],
            cardinality="single",
            temporal_behavior="current",
        )
    ]

    new_memory = Memory(
        id=None,
        category="learning",
        memory_key="goal",
        content="User wants to learn Java.",
        embedding=[0.3, 0.2, 0.3],
        cardinality="single",
        temporal_behavior="current",
    )

    result = memory_evolution._find_semantic_slot_match(
        new_memory,
        candidates,
    )

    assert result is None


def test_find_semantic_slot_match_returns_none_for_different_cardinality(
    memory_evolution,
):
    candidates = [
        Memory(
            id=uuid4(),
            category="interest",
            memory_key="hobby",
            content="User likes billiards.",
            embedding=[0.1, 0.2, 0.3],
            cardinality="multiple",
            temporal_behavior="current",
        )
    ]

    new_memory = Memory(
        id=None,
        category="interest",
        memory_key="hobby",
        content="User likes football.",
        embedding=[0.3, 0.2, 0.3],
        cardinality="single",
        temporal_behavior="current",
    )

    result = memory_evolution._find_semantic_slot_match(
        new_memory,
        candidates,
    )

    assert result is None


def test_should_update_single_current(
    memory_evolution,
):
    memory = Memory(
        content="User is focused on Java.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    candidate = Memory(
        id=uuid4(),
        content="User is focused on Python.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    assert memory_evolution._should_update(
        memory,
        candidate,
    )


def test_should_not_update_multiple(
    memory_evolution,
):
    memory = Memory(
        content="User likes football.",
        category="interest",
        memory_key="hobby",
        cardinality="multiple",
        temporal_behavior="current",
    )

    candidate = Memory(
        id=uuid4(),
        content="User likes billiards.",
        category="interest",
        memory_key="hobby",
        cardinality="multiple",
        temporal_behavior="current",
    )

    assert not memory_evolution._should_update(
        memory,
        candidate,
    )


def test_should_not_update_historical(
    memory_evolution,
):
    memory = Memory(
        content="User currently focuses on Java.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    candidate = Memory(
        id=uuid4(),
        content="User studied Python in 2025.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="historical",
    )

    assert not memory_evolution._should_update(
        memory,
        candidate,
    )


def test_same_content(memory_evolution):
    new_memory = Memory(
        content="Current, User is learning Python programming.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    candidate = Memory(
        id=uuid4(),
        content="User is learning Python",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    decision = memory_evolution._build_state_decision(
        memory=new_memory,
        candidate=candidate,
        candidate_index=0,
    )

    assert decision.action == MemoryAction.DUPLICATE
    assert decision.candidate_index == 0
    assert decision.resulting_content == None


def test_update_content(memory_evolution):
    new_memory = Memory(
        content="User is focused on learning Java.",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    candidate = Memory(
        id=uuid4(),
        content="User is learning Python",
        category="learning",
        memory_key="focus",
        cardinality="single",
        temporal_behavior="current",
    )

    decision = memory_evolution._build_state_decision(
        memory=new_memory,
        candidate=candidate,
        candidate_index=0,
    )

    assert decision.action == MemoryAction.UPDATE
    assert decision.candidate_index == 0
    assert decision.resulting_content == new_memory.content
