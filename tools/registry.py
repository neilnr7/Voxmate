
import inspect
import json
import types
from typing import get_type_hints, get_origin, get_args, Union


class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.metadata = {}

    def register(
        self,
        name,
        function,
        description=None,
        parameter_descriptions=None
    ):
        """
        Register a tool and its metadata.

        The function's docstring can provide its description.
        Type hints are used to generate parameter schemas.
        """

        description = (
            description
            or inspect.getdoc(function)
            or ""
        )

        self.tools[name] = function

        self.metadata[name] = {
            "description": description,
            "parameter_descriptions": parameter_descriptions or {}
        }

    def execute(self, name, arguments):
        if name not in self.tools:
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }

        try:
            result = self.tools[name](**arguments)

            return {
                "success": True,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_tools(self):
        return self.tools

    def _get_json_type(self, annotation):
        """Convert Python type hints into JSON Schema types."""

        origin = get_origin(annotation)
        args = get_args(annotation)

        if annotation is str:
            return {"type": "string"}

        if annotation is int:
            return {"type": "integer"}

        if annotation is float:
            return {"type": "number"}

        if annotation is bool:
            return {"type": "boolean"}

        if origin is list:
            item_type = args[0] if args else str
            return {
                "type": "array",
                "items": self._get_json_type(item_type)
            }

        if origin is dict:
            return {"type": "object"}

        if origin in (Union, types.UnionType):
            non_none_types = [
                arg for arg in args
                if arg is not type(None)
            ]

            if len(non_none_types) == 1:
                return self._get_json_type(non_none_types[0])

        raise TypeError(
            f"Unsupported or missing type annotation: {annotation}"
        )

    def get_tool_schema(self, name):
        """Generate one OpenAI-compatible tool schema."""

        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        function = self.tools[name]
        metadata = self.metadata[name]

        signature = inspect.signature(function)
        type_hints = get_type_hints(function)

        properties = {}
        required = []

        for param_name, param in signature.parameters.items():

            if param.kind not in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY
            ):
                continue

            annotation = type_hints.get(param_name)

            if annotation is None:
                raise TypeError(
                    f"Tool '{name}' parameter '{param_name}' "
                    "needs a type annotation."
                )

            properties[param_name] = self._get_json_type(annotation)

            param_description = metadata[
                "parameter_descriptions"
            ].get(param_name)

            if param_description:
                properties[param_name]["description"] = param_description

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": name,
                "description": metadata["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    def get_tool_schemas(self):
        """Generate schemas for all registered tools."""

        return [
            self.get_tool_schema(name)
            for name in self.tools
        ]
