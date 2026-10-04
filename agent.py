import json

from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry

from tools.apps import (
    open_app,
    close_app,
    focus_app,
    OPEN_APP_TOOL,
    CLOSE_APP_TOOL,
    FOCUS_APP_TOOL
)

from tools.browser import (
    open_url,
    search_web,
    get_page_text,
    go_back
)

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

from tools.input import (
    type_text,
    press_key,
    hotkey,
    click,
    scroll,
    TYPE_TEXT_TOOL,
    PRESS_KEY_TOOL,
    HOTKEY_TOOL,
    CLICK_TOOL,
    SCROLL_TOOL
)

from tools.screenshot import (
    take_screenshot,
    TAKE_SCREENSHOT_TOOL
)

OPEN_URL_TOOL = {
    "type": "function",
    "function": {
        "name": "open_url",
        "description": (
            "Open a website or web page. "
            "Use this when the user wants to open a website or web page. "
            "The user may optionally specify which browser to use. "
            "If a browser is specified, open the website using that browser. "
            "If no browser is specified, use the default browser."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": (
                        "The HTTP or HTTPS URL of the website or web page to open."
                    )
                },
                "browser": {
                    "type": "string",
                    "description": (
                        "Optional browser to use. "
                        "If not specified, use the default browser."
                    )
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

GET_PAGE_TEXT_TOOL = {
    "type": "function",
    "function": {
        "name": "get_page_text",
        "description": (
            "Get the readable text content from a webpage. "
            "Use this when the user asks to read, inspect, "
            "or get the text from a specific webpage."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The complete HTTP or HTTPS URL of the webpage."
                }
            },
            "required": ["url"]
        }
    }
}


GO_BACK_TOOL = {
    "type": "function",
    "function": {
        "name": "go_back",
        "description": (
            "Go back to the previous page in the browser. "
            "Use this when the user asks to go back, return to the "
            "previous webpage, or navigate backward."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


class Agent:
    def __init__(self):
        self.llm = LlamaClient()

        self.registry = ToolRegistry()

        # Application tools
        self.registry.register(
            "open_app",
            open_app
        )

        self.registry.register(
            "close_app",
            close_app
        )

        self.registry.register(
            "focus_app",
            focus_app
        )
        self.registry.register(
            "open_url",
            open_url
        )

        self.registry.register(
            "search_web",
            search_web
        )
        self.registry.register(
            "get_page_text",
            get_page_text
        )

        self.registry.register(
            "go_back",
            go_back
        )

        # System information tools
        self.registry.register(
            "get_time",
            get_time
        )

        self.registry.register(
            "get_date",
            get_date
        )

        self.registry.register(
            "get_battery",
            get_battery
        )

        # Clipboard tools
        self.registry.register(
            "read_clipboard",
            read_clipboard
        )

        self.registry.register(
            "write_clipboard",
            write_clipboard
        )

        self.registry.register(
            "clear_clipboard",
            clear_clipboard
        )

        # Input tools
        self.registry.register(
            "type_text",
            type_text
        )

        self.registry.register(
            "press_key",
            press_key
        )

        self.registry.register(
            "hotkey",
            hotkey
        )

        self.registry.register(
            "click",
            click
        )

        self.registry.register(
            "scroll",
            scroll
        )

        # Screenshot tool
        self.registry.register(
            "take_screenshot",
            take_screenshot
        )

        self.tools = [
            OPEN_APP_TOOL,
            CLOSE_APP_TOOL,
            FOCUS_APP_TOOL,

            
            OPEN_URL_TOOL,
            SEARCH_WEB_TOOL,
            GET_PAGE_TEXT_TOOL,
            GO_BACK_TOOL,


            GET_TIME_TOOL,
            GET_DATE_TOOL,
            GET_BATTERY_TOOL,

            READ_CLIPBOARD_TOOL,
            WRITE_CLIPBOARD_TOOL,
            CLEAR_CLIPBOARD_TOOL,

            TYPE_TEXT_TOOL,
            PRESS_KEY_TOOL,
            HOTKEY_TOOL,
            CLICK_TOOL,
            SCROLL_TOOL,

            TAKE_SCREENSHOT_TOOL
        ]

    def run(self, user_input):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are VoxMate, a Windows computer assistant. "

                    "Application control: "
                    "Use open_app when the user wants to open, start, launch, or run an application. "
                    "Use close_app when the user wants to close, quit, exit, or shut down an application. "
                    "Use focus_app when the user wants to focus, switch to, activate, bring to front, or show an application that is already running. "
                    "If the user asks to focus or switch to an application, use focus_app and do not use open_app. "

                    "Browser and web actions: "
                    "Browsers are applications, so use open_app to open, start, launch, or run any browser. "
                    "Do NOT use a separate browser-launching tool when opening a browser. "
                    "If the user mentions a website, web page, or URL, use open_url rather than open_app. "
                    "If the user provides an HTTP or HTTPS URL, always use open_url. "
                    "If the user specifies a browser together with a website or URL, pass that browser to open_url. "
                    "Use search_web when the user asks to search the web, look something up, or find information online. "
                    "Use get_page_text when the user asks to read or get the text/content of a webpage. "
                    "Use go_back when the user asks to go back in the browser. "

                    # General rule
                    "Choose the tool that most directly matches the user's request."
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