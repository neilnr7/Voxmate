import json

from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry
from tools.apps import open_app, OPEN_APP_TOOL


class Agent:
    def __init__(self):
        self.llm = LlamaClient()

        self.registry = ToolRegistry()

        self.registry.register(
            "open_app",
            open_app
        )

        self.tools = [
            OPEN_APP_TOOL
        ]

    def run(self, user_input):
        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.llm.chat(
            messages,
            tools=self.tools
        )

        if response.get("tool_calls"):
            tool_call = response["tool_calls"][0]

            tool_name = tool_call["function"]["name"]
            arguments = json.loads(
                tool_call["function"]["arguments"]
            )

            result = self.registry.execute(
                tool_name,
                arguments
            )

            return result

        return response.get("content")


if __name__ == "__main__":
    agent = Agent()

    response = agent.run("Open Chrome.")

    print(response)