import json


from tools.files import list_files, find_file, read_file, create_file
from pathlib import Path



from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry

from tools.apps import (
    open_app,
    close_app,
    focus_app,
    list_running_apps,
    OPEN_APP_TOOL,
    CLOSE_APP_TOOL,
    FOCUS_APP_TOOL,
    LIST_RUNNING_APPS_TOOL
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


class Agent:
    def __init__(self):
        self.llm = LlamaClient()

        self.registry = ToolRegistry()
        self.workspace = str(Path(__file__).resolve().parent)

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
            "list_running_apps",
            list_running_apps
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
            LIST_RUNNING_APPS_TOOL,

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


            LIST_FILES_TOOL,
            FIND_FILE_TOOL,
            READ_FILE_TOOL,
            CREATE_FILE_TOOL,

            TYPE_TEXT_TOOL,
            PRESS_KEY_TOOL,
            HOTKEY_TOOL,
            CLICK_TOOL,
            SCROLL_TOOL,

            TAKE_SCREENSHOT_TOOL

        ]

    


        # file tools
        self.registry.register("list_files", list_files)
        self.registry.register("find_file", find_file)
        self.registry.register("read_file", read_file)
        self.registry.register("create_file", create_file)



 

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
                "content": (
                    f"{user_input}\n\n"
                    f"Current workspace: {self.workspace}"
                )
            }
        ]

        response = self.llm.chat(
            messages,
            tools=self.tools
        )

        if response.get("tool_calls"):
            tool_call = response["tool_calls"][0]

            for tool_call in response["tool_calls"]:
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