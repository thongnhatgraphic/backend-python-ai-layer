from app.schemas.memory_decision_schema import MemoryDecision, MemoryAction
import json
from collections import Counter

relevant_ids = [2]

dense_ids = [1, 2, 3, 5, 6]

dense_hit = bool(set(dense_ids) & set(relevant_ids))
print(dense_hit)

memories = {
    "1": {"31715818"},
    "3": {"14717500"},
    "5": {"13734012"},
    "13": {"1606628"},
    "36": {"11705328", "5152028"},
    "42": {"18174210"},
    "48": {"13734012"},
    "49": {"5953485"},
    "50": {"12580014"},
    "51": {"45638119"},
    "53": {"45638119"},
    "54": {"49556906"},
    "56": {"4709641"},
    "57": {"4709641"},
    "70": {"4414547", "5956380"},
    "72": {"6076903"},
    "75": {"4387784"},
    "130": {"27768226"},
    "132": {"7975937"},
    "133": {"6969753", "17934082", "38485364", "16280642", "12640810"},
    "137": {"26016929"},
    "141": {"14437255", "6955746"},
    "142": {"10582939"},
    "143": {"10582939"},
}

result = Counter(len(docs) for docs in memories.values())

# print("----------", scores["memories"][:5])
# actual_indexes = {item["candidate_index"] for item in scores["memories"]}
# from app.tests.evaluation.reranker_eval_dataset import (
#     EVALUATION_DATASET,
# )

# results = {k: [] for k in CANDIDATE_K_VALUES}

# for index, item in enumerate(
#     EVALUATION_DATASET,
#     start=0,
# ):
#     query = item["query"]
#     relevant_ids = item["relevant_ids"]

#     print(f"\nQuery {index}: {query}")

# for k in CANDIDATE_K_VALUES:
#     print(f"\nK: {k}")

# seen = set()

# print(seen)


# expected_indexes = set(range(5))
# print(expected_indexes)
# print(actual_indexes)
# print(actual_indexes == expected_indexes)
