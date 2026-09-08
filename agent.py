import json

from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry
from tools.apps import open_app, OPEN_APP_TOOL
from tools.browser import open_browser
from tools.system import (
    get_time,
    get_date,
    get_battery,
    GET_TIME_TOOL,
    GET_DATE_TOOL,
    GET_BATTERY_TOOL
)

from tools.clipboard import (
    read_clipboard,
    write_clipboard,
    clear_clipboard,
    READ_CLIPBOARD_TOOL,
    WRITE_CLIPBOARD_TOOL,
    CLEAR_CLIPBOARD_TOOL
)

OPEN_BROWSER_TOOL = {
    "type": "function",
    "function": {
        "name": "open_browser",
        "description": (
            "Open a web browser. Use this tool whenever the user asks "
            "to open, start, launch, or run Chrome, Google Chrome, Edge, "
            "Microsoft Edge, or Firefox. If the user names one of these "
            "browsers, pass that browser name. If the user asks for a "
            "browser without specifying which one, leave the browser "
            "empty so the Windows default browser opens. Do NOT use "
            "open_app for Chrome, Edge, or Firefox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "browser": {
                    "type": "string",
                    "description": (
                        "The browser to open: Chrome, Edge, or Firefox. "
                        "Leave empty if the user does not specify a browser."
                    )
                }
            },
            "required": []
        }
    }
}


class Agent:
    def __init__(self):
        self.llm = LlamaClient()

        self.registry = ToolRegistry()

        self.registry.register(
            "open_app",
            open_app
        )

        self.registry.register(
            "open_browser",
            open_browser
        )

        self.tools = [
            OPEN_APP_TOOL,
            OPEN_BROWSER_TOOL,
            GET_TIME_TOOL,
            GET_DATE_TOOL,
            GET_BATTERY_TOOL,
            READ_CLIPBOARD_TOOL,
            WRITE_CLIPBOARD_TOOL,
            CLEAR_CLIPBOARD_TOOL
        ]
        #system info tools
        self.registry.register("get_time", get_time)
        self.registry.register("get_date", get_date)
        self.registry.register("get_battery", get_battery)
        
        #clipboard tools
        self.registry.register("read_clipboard", read_clipboard)
        self.registry.register("write_clipboard", write_clipboard)
        self.registry.register("clear_clipboard", clear_clipboard)

    def run(self, user_input):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are VoxMate, a Windows computer assistant. "
                    "Use open_browser for Chrome, Google Chrome, Edge, "
                    "Microsoft Edge, or Firefox. "
                    "Use open_app for other applications such as "
                    "Notepad or Calculator. "
                    "If the user asks to open a browser without "
                    "naming one, use open_browser with no browser specified."
                )
            },
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

    print("VoxMate started.")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("VoxMate shutting down.")
            break

        if not user_input.strip():
            continue

        response = agent.run(user_input)

        print("VoxMate:", response)
        print()