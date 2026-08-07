import math


# 1 token dot 1 token
def dot_product(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have same dimension")

    result = 0
    for x, y in zip(a, b):
        print(x, y)
        result += x * y

    return result


# dot với 1 key


query = [2, 1]
keys = [
    [2, 0],  # Redis
    [1, 1],  # is
    [0, 2],  # fast
]


# Dot product with all keys
def compare_query(query: list[float], keys: list[list[float]]) -> list[float]:
    scores = [dot_product(query, key) for key in keys]
    print("scores", scores)
    return scores


# Attention Scores
attention_scores = compare_query(query, keys)
print("attention_scores", attention_scores)


# Chia √dk
def scaled_scores(query: list[float], attention_scores: list[float]) -> list[float]:
    dimension = len(query)

    scaled_scores = [score / math.sqrt(dimension) for score in attention_scores]

    return scaled_scores


result_scaled_scores = scaled_scores(query, attention_scores)


#  Softmath
def softmax(scores: list[float]) -> list[float]:
    max_score = max(scores)

    exp_scores = [math.exp(score - max_score) for score in scores]

    total = sum(exp_scores)
    probabilities = [score / total for score in exp_scores]

    return probabilities


weights = softmax(result_scaled_scores)

print("weights", weights)


# Weighted Sum
values = [[8, 2], [3, 4], [6, 9]]


def weighted_sum(weights: list[float], values: list[list[float]]) -> list[float]:
    dimension = len(values[0])

    output = [0] * dimension

    for i in range(dimension):
        output[i] = sum(w * v[i] for w, v in zip(weights, values))

    return output


# result_weighted_sum [6.299964461206944, 3.5481955347861662]
print("result_weighted_sum", weighted_sum(weights, values))


# def calculated_weight_of_each_token_in_list_token(
#     query: list[float], keys: list[list[float]], values: list[list[float]]
# ) -> list[float]:
#     attention_scores = compare_query(query, keys)
#     scaled_scores = scaled_scores(query, attention_scores)
#     weights = softmax(scaled_scores)

#     weighted_sum_values = weighted_sum(weights, values)

#     return weighted_sum_values
