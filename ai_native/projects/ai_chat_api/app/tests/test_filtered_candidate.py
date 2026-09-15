import pytest

from app.schemas.memory_candidate_schema import MemoryCandidate
from app.schemas.memory_score_schema import MemoryScoreList, MemoryScore
from app.core.settings import settings
from app.services.chat_service import ChatService
from app.schemas.memory_semantics_schema import MemorySemantics


@pytest.fixture
def chat_service():
    return ChatService(
        memory=None,
        llm=None,
        ctx=None,
        memory_extractor=None,
        memory_store=None,
        memory_scorer=None,
        memory_evolution=None,
        embedding_service=None,
        reranker_service=None,
    )


def test_filter_candidates_keeps_relevant_candidates(chat_service):
    memory_scores = MemoryScoreList(
        memories=[
            MemoryScore(candidate_index=0, score=0.9),
            MemoryScore(candidate_index=1, score=0.8),
            MemoryScore(candidate_index=2, score=0.7),
        ]
    )
    memories: list[MemoryCandidate] = [
        MemoryCandidate(
            content="user is learning python",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
        MemoryCandidate(
            content="user is learning java",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
        MemoryCandidate(
            content="user is learning c sharp",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
    ]

    filtered_candidates = chat_service._filter_candidates(memory_scores, memories)

    assert len(filtered_candidates) == 3


def test_filter_candidates_removes_low_score_candidate(chat_service):
    # MEMORY_SAVE_THRESHOLD = 0.4 in .env
    memory_scores = MemoryScoreList(
        memories=[
            MemoryScore(candidate_index=0, score=0.9),
            MemoryScore(candidate_index=1, score=0.3),
            MemoryScore(candidate_index=2, score=0.7),
        ]
    )

    memories: list[MemoryCandidate] = [
        MemoryCandidate(
            content="user is learning python",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
        ),
        MemoryCandidate(
            content="user is learning java",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="historical",
            ),
        ),
        MemoryCandidate(
            content="user is learning c sharp",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
    ]

    filtered_candidates = chat_service._filter_candidates(memory_scores, memories)

    assert len(filtered_candidates) == 2
    assert filtered_candidates[0].content == "user is learning python"
    assert filtered_candidates[1].content == "user is learning c sharp"


def test_restore_index_order(chat_service):
    # MEMORY_SAVE_THRESHOLD = 0.4 in .env
    memory_scores = MemoryScoreList(
        memories=[
            MemoryScore(candidate_index=2, score=0.9),
            MemoryScore(candidate_index=0, score=0.3),
            MemoryScore(candidate_index=1, score=0.7),
        ]
    )

    memories: list[MemoryCandidate] = [
        MemoryCandidate(
            content="user is learning python",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
        MemoryCandidate(
            content="user is learning java",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
        MemoryCandidate(
            content="user is learning c sharp",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="event",
            ),
        ),
    ]

    filtered_candidates = chat_service._filter_candidates(memory_scores, memories)
    assert len(filtered_candidates) == 2
    assert filtered_candidates[0].content == "user is learning c sharp"
    assert filtered_candidates[1].content == "user is learning java"


def test_validate_scores_rejects_extra_candidate_index(
    scorer,
):
    memories = [
        MemoryCandidate(
            content="User is currently learning Python.",
            semantics=MemorySemantics(
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
        )
    ]

    scores = MemoryScoreList(
        memories=[
            MemoryScore(
                candidate_index=0,
                score=1.0,
            ),
            MemoryScore(
                candidate_index=1,
                score=0.0,
            ),
        ]
    )

    with pytest.raises(ValueError):
        scorer._validate_scores(
            scores,
            memories,
        )
