from app.services.embedding_service import EmbeddingService
from ollama import Client
from math import sqrt


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    # dot = sum(a * b for a, b in zip(v1, v2))

    # norm_v1 = sqrt(sum(x * x for x in v1))
    # norm_v2 = sqrt(sum(x * x for x in v2))

    # return dot / (norm_v1 * norm_v2)
    return sum(v1[i] * v2[i] for i in range(len(v1))) / (
        sqrt(sum(v1[i] ** 2 for i in range(len(v1))))
        * sqrt(sum(v2[i] ** 2 for i in range(len(v2))))
    )


cos = cosine_similarity(
    [
        0.0018999054,
        0.033671845,
        -0.16219006,
        -0.012549252,
        0.070499755,
        -0.051620353,
        0.015294694,
        0.014405401,
        -0.045551654,
        0.0139609855,
    ],
    [
        0.0038941063,
        0.07505314,
        -0.1651903,
        -0.015453388,
        -0.0054725804,
        -0.0073750857,
        -0.0019820598,
        0.07041595,
        -0.09093538,
        0.021822367,
    ],
)
print(cos)


def test_embedding_service() -> None:
    embedding_service = EmbeddingService(Client(host="http://localhost:11434"))

    embedding_service.embed("Tên của user là Nhất")

    embedding_service.embed("Tên tôi là gì?")


# test_embedding_service()
