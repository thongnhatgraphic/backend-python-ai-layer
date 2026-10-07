# Tool_raw = {
#     "type": "function",
#     "function": {
#         "name": "function_name",
#         "description": "description of the function",
#         "parameters": {
#               "type": "object",
#               "properties": {
#                   "input1": {"type": "string"}
#                   "input2": {"type": "string"}
#                   ...
#               },
#               "required": ["input1", "input2", ...]
#           },
#     },
# }
from pydantic import BaseModel
from typing import Callable


class ToolDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        input_model: type[BaseModel] | None,
        function: Callable,
        side_effect: bool = False,
        require_confirmation: bool = False,
    ):

        self.name = name
        self.description = description
        self.input_model = input_model
        self.function = function
        self.side_effect = side_effect
        self.require_confirmation = require_confirmation

    def to_llm_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_model.model_json_schema(),
            },
        }
