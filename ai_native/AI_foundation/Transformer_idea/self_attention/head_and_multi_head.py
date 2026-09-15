import math

queries = [[1, 2], [0, 1], [2, 1]]

keys = [[2, 1], [1, 1], [0, 2]]

values = [[10, 20], [30, 40], [50, 60]]

query = [2, 1]


def dot_product(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have same dimension")

    result = 0
    for x, y in zip(a, b):
        result += x * y

    return result


def compare_query(query: list[float], keys: list[list[float]]) -> list[float]:
    scores = [dot_product(query, key) for key in keys]

    return scores


def attention_scores(query, keys):
    return [dot_product(query, key) for key in keys]


def softmax(scores: list[float]) -> list[float]:
    max_score = max(scores)

    exp_scores = [math.exp(score - max_score) for score in scores]

    total = sum(exp_scores)
    probabilities = [score / total for score in exp_scores]

    return probabilities


def weighted_sum(weights: list[float], values: list[list[float]]) -> list[float]:
    dimension = len(values[0])

    output = [0] * dimension

    for i in range(dimension):
        output[i] = sum(w * v[i] for w, v in zip(weights, values))

    return output


def scaled_scores(query: list[float], attention_scores: list[float]) -> list[float]:
    dimension = len(query)

    scaled_scores = [score / math.sqrt(dimension) for score in attention_scores]

    return scaled_scores


def attention(
    query: list[float], keys: list[list[float]], values: list[list[float]]
) -> list[float]:
    scores = attention_scores(query, keys)
    weights = softmax(scores)
    weighted_sum_values = weighted_sum(weights, values)

    return weighted_sum_values


"""
    Compute self-attention output for a single query vector.

    Args:
        query: Query vector.
        keys: List of key vectors.
        values: List of value vectors.

    Returns:
        Weighted sum of value vectors.
"""


def self_attention(
    queries: list[list[float]],
    keys: list[list[list[float]]],
    values: list[list[list[float]]],
):
    output = []
    for query in queries:
        weighted_sum_values = attention(query, keys, values)
        output.append(weighted_sum_values)

    return output


""" This function computes the self-attention output for a batch of query vectors.

    Args:
        queries: List of query vectors.
        keys: List of key vectors.
        values: List of value vectors.

    Returns:
        List of weighted sum of value vectors for each query vector.

    Output is a single head of self-attention.
    """

self_attention(queries, keys, values)


def concatenate_heads(head_outputs: list[list[list[float]]]) -> list[list[float]]:
    output = []

    for token_index in range(len(head_outputs[0])):
        concatenated_vector = []

        for head in head_outputs:
            concatenated_vector.extend(head[token_index])

        output.append(concatenated_vector)
    print(output)
    return output


heads_example = [
    [[1, 2], [3, 4], [5, 6]],
    [[7, 8], [9, 10], [11, 12]],
    [[13, 14], [15, 16], [17, 18]],
    [[19, 20], [21, 22], [23, 24]],
]

concatenate_heads(heads_example)
