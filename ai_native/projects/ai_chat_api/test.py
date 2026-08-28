from app.schemas.memory_decision_schema import MemoryDecision, MemoryAction
import json

print("i am learning java".strip().casefold())


object_action = {
    MemoryAction.DUPLICATE,
    MemoryAction.UPDATE,
    MemoryAction.MERGE,
}

# access value of object_action
allowed_actions = set(MemoryAction)
print(allowed_actions)

allowed_action_names = {action.value.upper() for action in allowed_actions}
# Access attribute of allowed_actions
print("----", allowed_action_names)
print("----", sorted(allowed_action_names))


scores = {
    "memories": [
        {"candidate_index": 0, "score": 0.9},
        {"candidate_index": 1, "score": 0.8},
        {"candidate_index": 2, "score": 0.7},
        {"candidate_index": 3, "score": 0.6},
        {"candidate_index": 4, "score": 0.6},
    ]
}

actual_indexes = {item["candidate_index"] for item in scores["memories"]}
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
