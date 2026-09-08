import json



from tools.files import list_files, find_file



from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry
from tools.apps import open_app, OPEN_APP_TOOL
from tools.browser import open_browser, open_url, search_web
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
OPEN_URL_TOOL = {
    "type": "function",
    "function": {
        "name": "open_url",
        "description": (
            "Open a website or URL in the default web browser. "
            "Use this tool when the user asks to open a website, "
            "such as YouTube, GitHub, Google, or another website. "
            "The URL must be a valid HTTP or HTTPS URL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The complete HTTP or HTTPS URL to open."
                }
            },
            "required": ["url"]
        }
    }
}

SEARCH_WEB_TOOL = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": (
            "Search the web for information using a search engine. "
            "Use this when the user asks to search for something, "
            "look something up, or find information online."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"]
        }
    }
}


LIST_FILES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List files and folders inside a specified directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list."
                }
            },
            "required": ["path"]
        }
    }
}

FIND_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "find_file",
        "description": "Search for files whose names contain the given query inside a directory and its subdirectories.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The filename or part of the filename to search for."
                },
                "path": {
                    "type": "string",
                    "description": "The directory where the search should start."
                }
            },
            "required": ["query", "path"]
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
        self.registry.register(
            "open_url",
            open_url
        )
        self.registry.register(
            "search_web",
            search_web
        )

        self.tools = [
            OPEN_APP_TOOL,
            OPEN_BROWSER_TOOL,
            OPEN_URL_TOOL,
            SEARCH_WEB_TOOL,
            GET_TIME_TOOL,
            GET_DATE_TOOL,
            GET_BATTERY_TOOL,
            READ_CLIPBOARD_TOOL,
            WRITE_CLIPBOARD_TOOL,
            CLEAR_CLIPBOARD_TOOL,
            LIST_FILES_TOOL,
            FIND_FILE_TOOL
        ]
        #system info tools
        self.registry.register("get_time", get_time)
        self.registry.register("get_date", get_date)
        self.registry.register("get_battery", get_battery)
        
        #clipboard tools
        self.registry.register("read_clipboard", read_clipboard)
        self.registry.register("write_clipboard", write_clipboard)
        self.registry.register("clear_clipboard", clear_clipboard)

        # file tools
        self.registry.register("list_files", list_files)
        self.registry.register("find_file", find_file)

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