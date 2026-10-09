import json

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
    set_volume,
    mute_volume,
    unmute_volume,
    increase_volume,
    decrease_volume,
    set_brightness,
    increase_brightness,
    decrease_brightness,
    GET_TIME_TOOL,
    GET_DATE_TOOL,
    GET_BATTERY_TOOL,
    SET_VOLUME_TOOL,
    MUTE_VOLUME_TOOL,
    UNMUTE_VOLUME_TOOL,
    INCREASE_VOLUME_TOOL,
    DECREASE_VOLUME_TOOL,
    SET_BRIGHTNESS_TOOL,
    INCREASE_BRIGHTNESS_TOOL,
    DECREASE_BRIGHTNESS_TOOL
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

        #volume registry
        self.registry.register("set_volume", set_volume)
        self.registry.register("mute_volume", mute_volume)
        self.registry.register("unmute_volume", unmute_volume)
        self.registry.register("increase_volume", increase_volume)
        self.registry.register("decrease_volume", decrease_volume)

        #brightness registry
        self.registry.register("set_brightness", set_brightness)
        self.registry.register("increase_brightness", increase_brightness)
        self.registry.register("decrease_brightness", decrease_brightness)

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
            SET_VOLUME_TOOL,
            MUTE_VOLUME_TOOL,
            UNMUTE_VOLUME_TOOL,
            INCREASE_VOLUME_TOOL,
            DECREASE_VOLUME_TOOL,

            SET_BRIGHTNESS_TOOL,
            INCREASE_BRIGHTNESS_TOOL,
            DECREASE_BRIGHTNESS_TOOL,

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
                    "Use list_running_apps when the user asks to see, list, "
                    "or check which applications are currently running. "
                    "When a request requires opening or using an application that may already be running, first call list_running_apps and wait for its result. "
                    "Inspect the returned applications list before choosing the next action. "
                    "If any listed window title identifies the requested application, do not call open_app; call focus_app instead. "
                    "Only call open_app when the requested application is not present in the running applications list. "
                    "For a request to open a browser and search the web, check the running applications list first, focus the existing browser if it is listed, and then call search_web. "
                    "Do not call open_app and focus_app for the same application in one planned sequence. "
                    "When a user requests an action that requires typing into a specific application, ensure that application is in the foreground before calling type_text. "
                    "If the application is not already running, call open_app first. "
                    "After opening or identifying the application, call focus_app to bring its window to the foreground before typing. "
                    "Do not call type_text until the intended application has been focused successfully. "
                    "When focus_app reports failure, do not call type_text; stop the sequence and report the error. "
                    "When a request contains dependent actions, wait for the result of the earlier action before deciding which tool to call next. "


                     # Added: mandatory sequential tool execution
                    "Mandatory sequential tool execution: "
                    "When a task depends on the result of a previous tool, call only that tool in the current response. "
                    "Do not include dependent or subsequent tool calls in the same assistant response. "
                    "For application workflows, call list_running_apps by itself first, then wait for its tool result before deciding whether to call focus_app or open_app. "
                    "Wait for the result of focus_app or open_app before calling type_text or any other dependent action. "
                    "Call take_screenshot only after all requested preceding actions have completed successfully. "
                    "Never call focus_app and open_app together for the same application. "
                    "Never call type_text or take_screenshot before the preceding required actions have succeeded. "

                    "Browser and web actions: "
                    "Browser and web search coordination: "
                    "When the user asks to search the web, use search_web to perform the search. "
                    "Do not call open_app just because the user mentions a browser in a request that also asks for a web search, unless opening the browser itself is an explicit, separate requirement. "
                    "If the user explicitly asks to open a browser and then search, first call list_running_apps to check whether that browser is already running. "
                    "Wait for the list_running_apps result before choosing the next tool. "
                    "If the requested browser is already running, call focus_app to bring its existing window to the foreground. "
                    "If the requested browser is not running, call open_app to launch it. "
                    "After the browser has been focused or launched, perform the requested web search using search_web. "
                    "Do not call open_app and focus_app together for the same application. "
                    "Do not skip the running-app check just because multiple tools could be called in a single response. "

                    "If the user mentions a website, web page, or URL, use open_url rather than open_app. "
                    "If the user provides an HTTP or HTTPS URL, always use open_url. "
                    "If the user specifies a browser together with a website or URL, pass that browser to open_url. "
                    "Use search_web when the user asks to search the web, look something up, or find information online. "
                    "Use get_page_text when the user asks to read or get the text/content of a webpage. "
                    "Use go_back when the user asks to go back in the browser. "

                    # Volume control
                    "Use set_volume when the user asks to set, increase, decrease, "
                    "or change the system volume to a specific percentage. "
                    "Use mute_volume when the user asks to mute the system audio. "
                    "Use unmute_volume when the user asks to unmute the system audio. "

                    "Use increase_volume when the user asks to increase, raise, "
                    "turn up, or make the volume louder. "

                    "Use decrease_volume when the user asks to decrease, lower, "
                    "turn down, or make the volume quieter. "

                    # Brightness control
                    "Use set_brightness when the user asks to set the screen brightness "
                    "to a specific percentage. "

                    "Use increase_brightness when the user asks to increase, raise, "
                    "turn up, or make the brightness higher. "

                    "Use decrease_brightness when the user asks to decrease, lower, "
                    "turn down, or make the brightness lower. "


                    "General rule: "
                    "Choose the tool that most directly matches the user's request."
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        max_tool_steps = 5

        for _ in range(max_tool_steps):
            response = self.llm.chat(
                messages,
                tools=self.tools
            )
            print("LLM RESPONSE:", response)

            if not response.get("tool_calls"):
                return response.get("content")

            messages.append(response)

            
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["function"]["name"]

                print(f"\nEXECUTING TOOL: {tool_name}", flush=True)

                arguments = json.loads(
                    tool_call["function"]["arguments"]
                )

                print(f"ARGUMENTS: {arguments}", flush=True)

                result = self.registry.execute(
                    tool_name,
                    arguments
                )

                print(f"TOOL RESULT: {result}", flush=True)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result)
                })

                # Stop if the tool failed, including failures wrapped inside its result.
                tool_failed = (
                    result.get("success") is False
                    or (
                        isinstance(result.get("result"), dict)
                        and result["result"].get("success") is False
                    )
                )

                if tool_failed:
                    error_message = (
                        result.get("error")
                        or (
                            result["result"].get("error")
                            if isinstance(result.get("result"), dict)
                            else None
                        )
                        or f"Tool '{tool_name}' failed."
                    )

                    print(f"STOPPING TOOL SEQUENCE: {error_message}", flush=True)

                    return (
                        f"I couldn't complete the request because "
                        f"{tool_name} failed: {error_message}. "
                        "No further actions were executed."
                    )

        return "I could not complete the request within the allowed number of tool steps."



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