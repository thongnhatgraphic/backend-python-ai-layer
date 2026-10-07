from app.agent.idempotency.store import IdempotencyStore
from app.agent.tools.create_task.service import CreateTaskService

store = IdempotencyStore()
service = CreateTaskService(store)

result1 = service.create(
    title="Hello World",
    idempotency_key="operation-123",
)

result2 = service.create(
    title="Hello World",
    idempotency_key="operation-123",
)
print("count:", service.count)

result3 = service.create(
    title="Another Task",
    idempotency_key="operation-456",
)

print("result1:", result1)
print("result2:", result2)
print("result3:", result3)


print("count:", service.count)
