import json


from tools.files import list_files, find_file, read_file, create_file, write_file, rename_file, copy_file, move_file, delete_file, get_file_info
from pathlib import Path



from llm.llama_client import LlamaClient
from tools.registry import ToolRegistry

from tools.apps import (
    open_app,
    close_app,
    OPEN_APP_TOOL,
    CLOSE_APP_TOOL
)

from tools.browser import (
    open_browser,
    open_url,
    search_web
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

READ_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": (
            "Read and return the contents of a text file from the Windows computer. "
            "Use this when the user asks to read, show, or display the contents of a file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path of the file to read."
                }
            },
            "required": ["path"]
        }
    }
}

CREATE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Create a new empty file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path of the new file."
                }
            },
            "required": ["path"]
        }
    }
}

WRITE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file."
                }
            },
            "required": ["path", "content"]
        }
    }
}

RENAME_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "rename_file",
        "description": "Rename an existing file to a new name in the same directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path of the existing file."
                },
                "new_name": {
                    "type": "string",
                    "description": "The new filename."
                }
            },
            "required": ["path", "new_name"]
        }
    }
}

COPY_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "copy_file",
        "description": "Copy a file from one location to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "The complete path of the file to copy."
                },
                "destination": {
                    "type": "string",
                    "description": "The complete path where the copy should be created."
                }
            },
            "required": ["source", "destination"]
        }
    }
}

MOVE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "move_file",
        "description": "Move a file or folder from one location to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "The complete path of the file or folder to move."
                },
                "destination": {
                    "type": "string",
                    "description": "The destination path."
                }
            },
            "required": ["source", "destination"]
        }
    }
}

DELETE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": (
            "Delete a file or folder from the Windows computer. "
            "Use find_file first when the user provides only a filename "
            "without a complete path."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path of the file or folder to delete."
                },
                "recursive": {
                    "type": "boolean",
                    "description": (
                        "Set to true only when the user explicitly wants "
                        "a non-empty folder and all its contents deleted."
                    )
                }
            },
            "required": ["path"]
        }
    }
}

GET_FILE_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_file_info",
        "description": (
            "Get detailed information about a file or folder, "
            "including its name, type, extension, size, and timestamps. "
            "Use find_file first when the user provides only a filename "
            "without a complete path."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path of the file or folder."
                }
            },
            "required": ["path"]
        }
    }
}


class Agent:
    def __init__(self):
        self.llm = LlamaClient()

        self.registry = ToolRegistry()
        self.workspace = str(Path(__file__).resolve().parent)
        self.parent_workspace = str(Path(self.workspace).parent)

        # Application tools
        self.registry.register(
            "open_app",
            open_app
        )

        self.registry.register(
            "close_app",
            close_app
        )

        # Browser tools
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
            FIND_FILE_TOOL,
            READ_FILE_TOOL,
            CREATE_FILE_TOOL,
            WRITE_FILE_TOOL,
            RENAME_FILE_TOOL,
            COPY_FILE_TOOL,
            MOVE_FILE_TOOL,
            DELETE_FILE_TOOL,
            GET_FILE_INFO_TOOL,

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
        self.registry.register("write_file", write_file)
        self.registry.register("rename_file", rename_file)
        self.registry.register("copy_file", copy_file)
        self.registry.register("move_file", move_file)
        self.registry.register("delete_file", delete_file)
        self.registry.register("get_file_info", get_file_info)



 

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
                    "naming one, use open_browser with no browser specified. "
                    "Use the available tools to complete the user's request. "
                    "You may use multiple tools when necessary."
                    "When the user refers to the parent folder of the workspace, "
                    "use the parent folder path provided in the user context. "
                    
                    
                    "When a file is mentioned without a complete path, always use find_file "
                    "to locate it before moving, copying, renaming, deleting, reading, "
                    "or getting information about it. "
                    "Never guess or construct a file path yourself. "
                    "Use the exact path returned by find_file for the next tool. "
                    "Use the provided workspace PATH and parent folder PATH only as search locations."
                )
            },
            {
                "role": "user",
                "content": (
                    f"{user_input}\n\n"
                    f"Current workspace: {self.workspace}"
                    f"Parent folder: {self.parent_workspace}"
                )
            }
        ]

        while True:
            response = self.llm.chat(
                messages,
                tools=self.tools
            )

            if not response.get("tool_calls"):
                return response.get("content")

            for tool_call in response["tool_calls"]:
                tool_name = tool_call["function"]["name"]

                arguments = json.loads(
                    tool_call["function"]["arguments"]
                )

                if tool_name == "find_file" and not arguments.get("path"):
                    arguments["path"] = self.workspace

                result = self.registry.execute(
                    tool_name,
                    arguments
                )

                messages.append({
                    "role": "assistant",
                    "content": response.get("content", ""),
                    "tool_calls": response["tool_calls"]
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result)
                })


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