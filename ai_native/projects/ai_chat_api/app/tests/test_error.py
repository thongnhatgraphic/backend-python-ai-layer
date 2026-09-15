import json
from app.schemas.memory_schema import Memory, MemoryList
from typing import Literal, TypeVar

T = TypeVar("T")


response = '{"content": "Tên tôi là Nhất"}'

# result = json.loads(response)

# print("result", result)


def test_error(response_model: type[T]):
    try:
        print("response", response_model.model_json_schema())

        memory_data = json.loads(response)
    except json.JSONDecodeError:
        return []

    print("memory_data", memory_data)

    if not isinstance(memory_data, list):
        print("not list")
        return []
    print("type", type(memory_data))


def test_list():
    list_Arr = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]
    return [*list_Arr]


print(test_list())
