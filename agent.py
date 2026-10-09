import os
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

from tools.files import (
    list_files,
    find_file,
    read_file,
    create_file,
    write_file,
    rename_file,
    copy_file,
    move_file,
    delete_file,
    get_file_info,
    create_folder,
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



LIST_FILES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List files and folders in a specified directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list."}
            },
            "required": ["path"]
        }
    }
}

FIND_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "find_file",
        "description": "Recursively search for files by full or partial filename.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Filename or part of filename."},
                "path": {"type": "string", "description": "Directory in which to search."}
            },
            "required": ["query", "path"]
        }
    }
}

READ_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read."}
            },
            "required": ["path"]
        }
    }
}

CREATE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Create a new empty file without overwriting an existing file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path for the new file."}
            },
            "required": ["path"]
        }
    }
}

WRITE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write text content to a file, creating it or overwriting its contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path."},
                "content": {"type": "string", "description": "Text to write."}
            },
            "required": ["path", "content"]
        }
    }
}

RENAME_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "rename_file",
        "description": "Rename an existing file within its current directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Existing file path."},
                "new_name": {"type": "string", "description": "New filename only."}
            },
            "required": ["path", "new_name"]
        }
    }
}

COPY_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "copy_file",
        "description": "Copy a file to a destination path or existing destination directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source file path."},
                "destination": {"type": "string", "description": "Destination path or directory."}
            },
            "required": ["source", "destination"]
        }
    }
}

MOVE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "move_file",
        "description": "Move a file or folder to a destination path or existing directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source file or folder path."},
                "destination": {"type": "string", "description": "Destination path or directory."}
            },
            "required": ["source", "destination"]
        }
    }
}

CREATE_FOLDER_TOOL = {
    "type": "function",
    "function": {
        "name": "create_folder",
        "description": (
            "Create a folder at the specified path. "
            "Use an absolute path when the user refers to "
            "the VoxMate project folder."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Full path of the folder to create."
                    ),
                }
            },
            "required": ["path"],
        },
    },
}


DELETE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Delete a file or folder. Recursive deletion must only be used when explicitly requested.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or folder path to delete."},
                "recursive": {"type": "boolean", "description": "Delete a folder and its contents only when explicitly requested. Defaults to false."}
            },
            "required": ["path"]
        }
    }
}

GET_FILE_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_file_info",
        "description": "Get a file or folder's name, type, extension, size, and timestamps.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or folder path."}
            },
            "required": ["path"]
        }
    }
}



def format_file_info(result):
    """Format get_file_info output into a readable response."""

    # Handle registry-wrapped results.
    if isinstance(result, dict) and isinstance(result.get("result"), dict):
        result = result["result"]

    if not isinstance(result, dict):
        return None

    if not result.get("success"):
        error = result.get("error", "Unknown error.")
        return f"Could not retrieve file information: {error}"

    return (
        "File information:\n"
        f"Path: {result.get('path', 'Unknown')}\n"
        f"Name: {result.get('name', 'Unknown')}\n"
        f"Type: {result.get('type', 'Unknown')}\n"
        f"Extension: {result.get('extension') or 'None'}\n"
        f"Size: {result.get('size_bytes', 'Unknown')} bytes\n"
        f"Created: {result.get('created', 'Unknown')}\n"
        f"Modified: {result.get('modified', 'Unknown')}\n"
        f"Accessed: {result.get('accessed', 'Unknown')}"
    )


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

        #File registry
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
        self.registry.register("create_folder",create_folder)


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

            TAKE_SCREENSHOT_TOOL,

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
            CREATE_FOLDER_TOOL,
        ]

    def run(self, user_input):
        project_root = os.path.dirname(os.path.abspath(__file__))
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


                    # File management
                    "File management: "
                    "Understand the user's intended file operation from the meaning "
                    "of the request, not just specific keywords. Adapt to different "
                    "wording, filenames, paths, and folder names. "

                    f"The VoxMate project root is: {project_root}. "
                    "When the user says 'project folder', 'project directory', "
                    "'VoxMate folder', or 'the project', use this exact path. "
                    "Do not interpret these phrases as literal directory names. "
                    "When a filename is provided without a directory, resolve it "
                    "relative to the project root unless the user specifies another location. "


                    "When the user asks to list the project folder, call list_files "
                    "with the exact VoxMate project root path. "
                    "When the user asks to find a file in the project folder, call "
                    "find_file with the filename as query and the exact project root "
                    "path as path. "
                    "For relative file paths, interpret them relative to the project "
                    "root unless the user specifies another directory. "
                    "Never pass phrases such as 'project folder' or 'current folder' "
                    "as literal filesystem paths. "

                    "Choose the most appropriate file-management tool for the task. "
                    "Use list_files to inspect a directory, find_file to search "
                    "recursively by filename or partial filename, read_file to read "
                    "text content, create_file to create an empty file, write_file "
                    "to write content, rename_file to rename, copy_file to copy, "
                    "move_file to move, delete_file to delete, and get_file_info "
                    "to retrieve metadata. "

                    "When the user asks for file information, file details, properties, "
                    "size, extension, or timestamps, you MUST call get_file_info. "

                    "If the file is identified only by filename, first call find_file. "
                    "Then call get_file_info using the exact path returned by find_file. "
                    "Do not treat finding the file as completing a request for its metadata. "
                    "Do not ask the user whether they want size or other details when they "
                    "have already requested file information. "

                    "Resolve missing source paths before performing file operations. "
                    "When only a filename is provided, use find_file with the most "
                    "relevant search directory available from the user's request "
                    "and context. Use the exact returned path; never invent paths. "

                    "Determine source and destination from the user's intent. "
                    "Use the specified directory when provided. Do not confuse a "
                    "destination folder with a destination filename. "

                    "For tasks requiring multiple operations, call tools in the "
                    "necessary order, use earlier results as inputs to later calls, "
                    "and continue until the requested task is complete. Avoid "
                    "unnecessary tool calls. If a search returns multiple plausible "
                    "matches, do not arbitrarily choose one when the intended file "
                    "is unclear. "

                    "Check tool results before reporting success. If a tool fails, "
                    "use its error to determine whether a safe alternative or another "
                    "search is appropriate. Never claim an operation succeeded when "
                    "the result indicates failure. "
                    "FOLDER MANAGEMENT RULES: "
                    "When the user asks to create a folder, use the create_folder tool "
                    "with the full folder path. "
                    "When the user asks to create a folder and then move a file into it, "
                    "call create_folder first, then call move_file using the source file "
                    "path and destination folder path. "
                    "Do not call move_file until create_folder succeeds, unless the "
                    "destination folder already exists. "
                    "If create_folder fails, do not call move_file. Explain the error "
                    "to the user. "
                    "Use the VoxMate project root as the base directory when the user "
                    "says 'in the project folder'. "
                    "Never claim a folder was created or a file was moved unless the "
                    "corresponding tool result confirms success. "



                    "Use recursive deletion only when the user explicitly requests "
                    "deleting a folder and its contents. Never overwrite or delete "
                    "existing data unless the requested operation clearly calls for it. "
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]


        max_tool_steps = 5

        metadata_phrases = (
            "file information",
            "file info",
            "file details",
            "file properties",
            "show information",
            "get information",
            "metadata",
        )

        is_metadata_request = any(
            phrase in user_input.casefold()
            for phrase in metadata_phrases
        )

        for _ in range(max_tool_steps):
            response = self.llm.chat(
                messages,
                tools=self.tools
            )

            print("LLM RESPONSE:", response)

            tool_calls = response.get("tool_calls")
            content = response.get("content")

            # Return a normal final response when available.
            if not tool_calls:
                if isinstance(content, str) and content.strip():
                    return content

                # Ask the model to produce a useful final response.
                messages.append(response)
                messages.append({
                    "role": "user",
                    "content": (
                        "Provide a useful final response to the original "
                        "request using the available tool results. "
                        "Do not claim success without evidence."
                    )
                })
                continue

            # Preserve the assistant message containing tool calls.
            messages.append(response)


            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                raw_arguments = tool_call["function"].get(
                    "arguments", "{}"
                )

                try:
                    if isinstance(raw_arguments, str):
                        arguments = json.loads(raw_arguments)
                    elif isinstance(raw_arguments, dict):
                        arguments = raw_arguments
                    else:
                        raise ValueError(
                            "Tool arguments must be a JSON object."
                        )

                    if not isinstance(arguments, dict):
                        raise ValueError(
                            "Tool arguments must be a JSON object."
                        )

                except (json.JSONDecodeError, ValueError) as e:
                    print(
                        f"INVALID TOOL ARGUMENTS for {tool_name}: "
                        f"{raw_arguments}"
                    )
                    result = {
                        "success": False,
                        "error": f"Invalid tool arguments: {e}",
                    }

                else:
                    print(
                        f"\nEXECUTING TOOL: {tool_name}",
                        flush=True
                    )
                    print(f"ARGUMENTS: {arguments}", flush=True)

                    result = self.registry.execute(
                        tool_name,
                        arguments
                    )

                print(
                    "TOOL RESULT:",
                    json.dumps(result, indent=2, default=str),
                    flush=True
                )

                if (
                    tool_name == "find_file"
                    and is_metadata_request
                ):
                    search_result = result

                    if (
                        isinstance(search_result, dict)
                        and isinstance(search_result.get("result"), dict)
                    ):
                        search_result = search_result["result"]

                    if not isinstance(search_result, dict):
                        return (
                            "Could not interpret the file search result."
                        )

                    if not search_result.get("success"):
                        return (
                            "File search failed: "
                            + search_result.get(
                                "error", "Unknown error."
                            )
                        )

                    matches = search_result.get("matches", [])

                    if not matches:
                        return (
                            f"No file matching "
                            f"'{arguments.get('query', '')}' was found."
                        )

                    if len(matches) > 1:
                        return (
                            f"Found {len(matches)} matching files. "
                            "Please specify which file you want "
                            "information about:\n"
                            + "\n".join(
                                f"- {match}" for match in matches
                            )
                        )

                    info_result = self.registry.execute(
                        "get_file_info",
                        {"path": matches[0]}
                    )

                    print(
                        "TOOL RESULT (get_file_info):",
                        json.dumps(
                            info_result,
                            indent=2,
                            default=str
                        ),
                        flush=True
                    )

                    formatted = format_file_info(info_result)

                    if formatted is not None:
                        return formatted

                    return (
                        "The file was found, but its metadata "
                        "could not be formatted."
                    )

                if tool_name == "get_file_info":
                    formatted = format_file_info(result)

                    if formatted is not None:
                        return formatted

                tool_failed = (
                    isinstance(result, dict)
                    and (
                        result.get("success") is False
                        or (
                            isinstance(result.get("result"), dict)
                            and result["result"].get("success") is False
                        )
                    )
                )

                if tool_failed:
                    inner_result = result.get("result")
                    error_message = (
                        result.get("error")
                        or (
                            inner_result.get("error")
                            if isinstance(inner_result, dict)
                            else None
                        )
                        or f"Tool '{tool_name}' failed."
                    )

                    print(
                        f"STOPPING TOOL SEQUENCE: {error_message}",
                        flush=True
                    )

                    return (
                        f"I couldn't complete the request because "
                        f"{tool_name} failed: {error_message}. "
                        "No further actions were executed."
                    )

                llm_result = result

                if isinstance(result, dict):
                    inner_result = result.get("result")

                    if (
                        tool_name == "read_file"
                        and isinstance(inner_result, dict)
                    ):
                        content = inner_result.get("content")

                        if isinstance(content, str) and len(content) > 4000:
                            inner_result = inner_result.copy()
                            inner_result["content"] = (
                                content[:4000]
                                + "\n\n[Content truncated for context "
                                + f"limits. Original length: {len(content)} "
                                + "characters.]"
                            )

                            llm_result = result.copy()
                            llm_result["result"] = inner_result

                    elif (
                        tool_name == "read_file"
                        and isinstance(result.get("content"), str)
                    ):
                        content = result["content"]

                        if len(content) > 4000:
                            llm_result = result.copy()
                            llm_result["content"] = (
                                content[:4000]
                                + "\n\n[Content truncated for context "
                                + f"limits. Original length: {len(content)} "
                                + "characters.]"
                            )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(llm_result, default=str)
                })

        return (
            "I could not complete the request within the allowed "
            "number of tool steps."
        )






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
