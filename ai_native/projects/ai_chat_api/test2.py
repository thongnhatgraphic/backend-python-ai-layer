from app.schemas.context_schemas.context_candidate import ContextCandidate
from app.context.context_priority import ContextImportance

# candidates = [
#     ContextCandidate(
#         name="memory",
#         tokens=0,
#         priority="HIGH",
#     ),
#     ContextCandidate(
#         name="rag",
#         tokens=0,
#         priority="LOW",
#     ),
#     ContextCandidate(
#         name="history",
#         tokens=0,
#         priority="NONE",
#     ),
# ]

raw_allocations = {"memory_demand": 300, "rag_demand": 500, "history_demand": 200}

# sorted_data = sorted(candidates, key=lambda item: weights[item.priority])

# print(sorted_data)

sor = raw_allocations.items()
print(sor)
for item in sor:
    print(item[0], item[1])
