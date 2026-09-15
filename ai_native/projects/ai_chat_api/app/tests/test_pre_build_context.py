import pytest
from app.schemas.memory_rerank_schema import MemoryRerankResult
from app.schemas.memory_schema import Memory
from app.services.context_builder import ContextBuilder


@pytest.fixture
def token_counter():
    class FakeTokenCounter:
        def count(self, text: str) -> int:
            return len(text.split())

    return FakeTokenCounter()


@pytest.fixture
def context_builder(token_counter):

    return ContextBuilder(
        token_counter=token_counter,
        max_retrieved_context_tokens=50,
        semantic_dedup_threshold=0.90,
    )


def test_cosine_similarity_identical_vectors(
    context_builder,
):
    score = context_builder._cosine_similarity(
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    )
    print(score)
    assert score == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors(
    context_builder,
):
    score = context_builder._cosine_similarity(
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    )
    print(score)
    assert score == pytest.approx(0.0)


def test_deduplicate_semantic_duplicates(
    context_builder,
):
    memories = [
        MemoryRerankResult(
            memory=Memory(
                content="I am learning Python.",
                embedding=[1.0, 0.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.95,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="I am currently studying Python programming.",
                embedding=[0.99, 0.01, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.94,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="I am learning Java.",
                embedding=[0.0, 1.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.90,
        ),
    ]

    result = context_builder._deduplicate_memories(memories)

    assert len(result) == 2

    assert result[0].memory.content == ("I am learning Python.")

    assert result[1].memory.content == ("I am learning Java.")


# def test_fit_to_token_budget(context_builder):
#     memories = [
#         MemoryRerankResult(
#             memory=Memory(
#                 content="i am learning python. Python hard to learn good.",
#                 embedding=[1.0, 0.0, 0.0],
#                 category="learning",
#                 memory_key="focus",
#                 cardinality="single",
#                 temporal_behavior="current",
#             ),
#             score=0.95,
#         ),
#         MemoryRerankResult(
#             memory=Memory(
#                 content="i am learning java. Java hard to learn good.",
#                 embedding=[0.0, 1.0, 0.0],
#                 category="learning",
#                 memory_key="focus",
#                 cardinality="single",
#                 temporal_behavior="current",
#             ),
#             score=0.94,
#         ),
#         MemoryRerankResult(
#             memory=Memory(
#                 content="java and python are programing languages that I interests in learning",
#                 embedding=[0.99, 0.01, 0.0],
#                 category="learning",
#                 memory_key="focus",
#                 cardinality="single",
#                 temporal_behavior="current",
#             ),
#             score=0.94,
#         ),
#     ]

#     selected_memories = context_builder._fit_to_token_budget(memories)

#     assert len(selected_memories) == 2

#     assert (
#         selected_memories[0].memory.content
#         == "i am learning python. Python hard to learn good."
#     )
#     assert (
#         selected_memories[1].memory.content
#         == "i am learning java. Java hard to learn good."
#     )

#     assert selected_memories[0].score == 0.95
#     assert selected_memories[1].score == 0.94


def test_build_uses_deduplicated_and_budgeted_memories(context_builder):
    memories = [
        MemoryRerankResult(
            memory=Memory(
                content="i am learning python. Python hard to learn good.",
                embedding=[1.0, 0.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.95,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="i am learning java. Java hard to learn good.",
                embedding=[0.0, 1.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.94,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="java and python are programing languages that I interests in learning",
                embedding=[0.99, 0.01, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.94,
        ),
    ]

    memories_deduplicated = context_builder._deduplicate_memories(memories)
    print("\nselected_memories \n", memories_deduplicated)
    assert len(memories_deduplicated) == 2

    memories_context = context_builder._fit_to_token_budget(memories_deduplicated)
    print("\nmemories_context \n", memories_context)
    assert len(memories_context) == 2
    assert memories_context[0].memory.content == memories[0].memory.content
    assert memories_context[1].memory.content == memories[1].memory.content


def test_build(context_builder):
    memories = [
        MemoryRerankResult(
            memory=Memory(
                content="I am learning Python.",
                embedding=[1.0, 0.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.95,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="I am currently studying Python programming.",
                embedding=[0.99, 0.01, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.94,
        ),
        MemoryRerankResult(
            memory=Memory(
                content="I am learning Java.",
                embedding=[0.0, 1.0, 0.0],
                category="learning",
                memory_key="focus",
                cardinality="single",
                temporal_behavior="current",
            ),
            score=0.90,
        ),
    ]

    history = [
        {
            "role": "user",
            "content": "Tôi đang học gì?",
        },
        {
            "role": "assistant",
            "content": "Bạn đang học Python.",
        },
    ]

    user_message = "Tôi đang tập trung học gì?"

    result = context_builder.build(
        history=history,
        memories=memories,
        user_message=user_message,
    )

    print("\nRESULT: 0\n", result[0])
    print("\nRESULT: 1\n", result[-1])
    print("\nRESULT: -2\n", result[2])
    assert result[0]["role"] == "system"
    assert result[-1]["role"] == "user"
    assert result[-1]["content"] == user_message
