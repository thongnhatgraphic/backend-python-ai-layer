import pytest

from app.context.context_allocator import ContextAllocator
from app.context.context_priority import ContextImportance

from app.schemas.context_schemas.context_candidate import ContextCandidate

# from app.core.settings import settings


# python -m pytest app/tests/context/test_context_allocator.py -v
@pytest.fixture
def allocator():
    return ContextAllocator()


def test_priority_allocation(allocator):
    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=2000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=7000,
            priority=ContextImportance.MEDIUM,
        ),
        ContextCandidate(
            max_tokens=3000,
            name="history",
            demand_tokens=6000,
            priority=ContextImportance.LOW,
        ),
    ]

    allocation = allocator.allocate(10000, candidates)

    assert allocation.memory_tokens == 2000
    assert allocation.rag_tokens == 7000
    assert allocation.history_tokens == 1000
    assert allocation.total_tokens == 10000


def test_budget_smaller_than_high_priority_candidate(allocator):
    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=6000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            demand_tokens=3000,
            max_tokens=4000,
            priority=ContextImportance.LOW,
        ),
    ]

    result = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )
    print("\n\n result \n\n", result)
    assert result.memory_tokens == 5000
    assert result.rag_tokens == 0


def test_zero_budget(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=2000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=3000,
            priority=ContextImportance.MEDIUM,
        ),
    ]

    result = allocator.allocate(
        budget=0,
        candidates=candidates,
    )

    assert result.memory_tokens == 0
    assert result.rag_tokens == 0
    assert result.history_tokens == 0


def test_allocate_respects_budget(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=2000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=6000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="history",
            max_tokens=3000,
            demand_tokens=1000,
            priority=ContextImportance.MEDIUM,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.total_tokens == 5000


def test_allocate_never_exceeds_demand():
    allocator = ContextAllocator()

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=500,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=6000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="history",
            demand_tokens=1000,
            priority=ContextImportance.MEDIUM,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.memory_tokens <= 500
    assert allocation.rag_tokens <= 6000
    assert allocation.history_tokens <= 1000


def test_none_context_gets_zero(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=2000,
            priority=ContextImportance.NONE,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.memory_tokens == 0
    assert allocation.rag_tokens == 3000


def test_small_high_priority_demand_is_fully_satisfied(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=500,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=6000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="history",
            demand_tokens=1000,
            priority=ContextImportance.MEDIUM,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.memory_tokens == 500


def test_same_priority_is_not_order_dependent(allocator):

    candidates_a = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
    ]

    candidates_b = [
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
    ]

    allocation_a = allocator.allocate(
        budget=4000,
        candidates=candidates_a,
    )

    allocation_b = allocator.allocate(
        budget=4000,
        candidates=candidates_b,
    )

    assert allocation_a.memory_tokens == allocation_b.memory_tokens
    assert allocation_a.rag_tokens == allocation_b.rag_tokens


def test_same_priority_demand_is_split_fairly(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            demand_tokens=3000,
            priority=ContextImportance.HIGH,
        ),
    ]

    allocation = allocator.allocate(
        budget=4000,
        candidates=candidates,
    )

    assert allocation.memory_tokens == 2000
    assert allocation.rag_tokens == 2000


def test_max_tokens_caps_demand(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            max_tokens=5000,
            max_tokens=1000,
            priority=ContextImportance.HIGH,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.memory_tokens == 1000


def test_medium_does_not_take_budget_from_high(allocator):

    candidates = [
        ContextCandidate(
            name="memory",
            max_tokens=1500,
            max_tokens=1500,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="rag",
            max_tokens=4000,
            max_tokens=4000,
            priority=ContextImportance.HIGH,
        ),
        ContextCandidate(
            name="history",
            max_tokens=1000,
            priority=ContextImportance.MEDIUM,
        ),
    ]

    allocation = allocator.allocate(
        budget=5000,
        candidates=candidates,
    )

    assert allocation.history_tokens == 0
    assert allocation.total_tokens == 5000
