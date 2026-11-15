import os

import json

import re

import time

from llm.llama_client import LlamaClient

from tools.registry import ToolRegistry

from tools.router import SemanticToolRouter



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



        """self.tools = [

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

        ]"""



        self.tools = self.registry.get_tool_schemas()

        self.router = SemanticToolRouter(self.registry)



    def run(self, user_input):

        agent_start_time = time.perf_counter()

        print(f"USER INPUT: {user_input}", flush=True)



        llm_timings = []

        tool_timings = []



        llm_token_totals = {

            "prompt_tokens": 0,

            "completion_tokens": 0,

            "total_tokens": 0

        }



        def print_performance_summary():

            total_llm_time = sum(llm_timings)

            total_tool_time = sum(

                duration for _, duration in tool_timings

            )

            total_agent_time = time.perf_counter() - agent_start_time



            print("\n========== VOXMATE PERFORMANCE ==========", flush=True)



            print("\nLLM:", flush=True)



            for index, duration in enumerate(llm_timings, start=1):

                print(

                    f"  LLM Call {index}: {duration:.3f} sec",

                    flush=True

                )



            print(

                f"  Total LLM time: {total_llm_time:.3f} sec",

                flush=True

            )



            print(

                f"  Total LLM calls: {len(llm_timings)}",

                flush=True

            )



            print("\nLLM TOKEN USAGE:", flush=True)



            print(

                f"  Prompt tokens: "

                f"{llm_token_totals['prompt_tokens']}",

                flush=True

            )



            print(

                f"  Completion tokens: "

                f"{llm_token_totals['completion_tokens']}",

                flush=True

            )



            print(

                f"  Total tokens: "

                f"{llm_token_totals['total_tokens']}",

                flush=True

            )



            print("\nTOOLS:", flush=True)



            for tool_name, duration in tool_timings:

                print(

                    f"  {tool_name}: {duration:.3f} sec",

                    flush=True

                )



            print(

                f"  Total tool time: {total_tool_time:.3f} sec",

                flush=True

            )



            print("\nAGENT:", flush=True)



            print(

                f"  Total processing time: {total_agent_time:.3f} sec",

                flush=True

            )



            print("\n==========================================\n", flush=True)



        project_root = os.path.dirname(os.path.abspath(__file__))

        messages = [

            {

                "role": "system",



                "content": f"""

                You are VoxMate, a Windows desktop voice assistant.



                GENERAL RULES:

                - Understand the user's intent, not just keywords.

                - Select the most appropriate available tool.

                - Never claim an action succeeded unless its tool result confirms success.

                - If a tool fails, explain the error and do not continue dependent actions.

                - Avoid unnecessary tool calls.

                - Give concise, natural, conversational responses suitable for speech.

                - Do not unnecessarily read out technical paths or internal execution details.



                APPLICATION CONTROL:

                - open_app launches an application or focuses it if already running.

                - Use close_app to close an application.

                - Use focus_app to switch to or activate an already-running application.

                - Use list_running_apps only when the user asks which applications are running.

                - Never call open_app and focus_app together for the same application.

                - Do not call list_running_apps before open_app.

                - For actions requiring typing into an application, first call open_app and verify success before using type_text.



                BROWSER AND WEB:

                - Use open_url for websites and URLs.

                - Use search_web for web searches and online information.

                - Use get_page_text to retrieve webpage content.

                - Use go_back to navigate to the previous webpage.

                - A web search does not require opening a browser unless explicitly requested.

                - If the user explicitly asks to open a browser and then search, open/focus it first and wait for success.

                - Pass an explicitly requested browser to open_url or search_web.

                - Supported browser names: edge, chrome, firefox, brave, opera.

                - Without a specified browser, use the Windows default browser.



                SYSTEM CONTROLS:

                - Use get_time, get_date, and get_battery for time, date, and battery information.

                - Use set_volume for a specific volume percentage.

                - Use increase_volume and decrease_volume for relative changes.

                - Use mute_volume and unmute_volume for muting and unmuting.

                - Use set_brightness for a specific brightness percentage.

                - Use increase_brightness and decrease_brightness for relative changes.



                FILE MANAGEMENT:

                The VoxMate project root is: {project_root}



                - Interpret "project folder", "VoxMate folder", and "the project" as the exact project root above.

                - Resolve relative file paths against the project root unless another location is specified.

                - Never treat phrases such as "project folder" or "current folder" as literal paths.

                - Use list_files to list directory contents.

                - Use find_file to search recursively by filename.

                - Use read_file to read text contents.

                - Use create_file to create an empty file.

                - Use write_file to write or overwrite file contents.

                - Use rename_file to rename a file.

                - Use copy_file to copy files.

                - Use move_file to move files or folders.

                - Use delete_file to delete files or folders.

                - Use get_file_info to retrieve file metadata.

                - Use create_folder to create folders.



                FILE OPERATION RULES:

                - When a user requests file information using only a filename, first call find_file, then call get_file_info using the exact returned path.

                - Do not claim that finding a file completes a metadata request.

                - Never invent file paths.

                - Determine source and destination from the user's intent.

                - Distinguish destination folders from destination filenames.

                - If multiple plausible files are found, ask the user to identify the intended file.

                - For dependent operations, use the exact result of the earlier operation as input to the next.

                - When creating a folder and moving a file into it, create the folder first and verify success before moving the file.

                - Never continue a dependent sequence after a failed operation.

                - Use recursive deletion only when explicitly requested.

                - Never overwrite or delete existing data unless the requested operation clearly requires it.



                SEQUENTIAL EXECUTION:

                - Execute only the next required tool call when an operation depends on a previous result.

                - Wait for its result before deciding the next operation.

                - Do not issue dependent tool calls together.

                - Execute independent actions only when they do not depend on one another.

                - Take screenshots only after the requested preceding actions succeed.

                - Continue until the user's request is completed or a failure requires stopping.

                """



            },

            {

                "role": "user",

                "content": user_input

            }

        ]

        system_prompt = messages[0]["content"]



        print(

            f"SYSTEM PROMPT SIZE: {len(system_prompt)} characters",

            flush=True

        )



        print(

            f"SYSTEM PROMPT WORDS: {len(system_prompt.split())}",

            flush=True

        )





        try:

            selected_tools = self.router.select_tools(

                user_input,

                tools_per_part=2

            )



            selected_tool_names = {

                tool["name"] for tool in selected_tools

            }



            available_tools = [

                tool for tool in self.tools

                if tool["function"]["name"] in selected_tool_names

            ]



            if not available_tools:

                available_tools = self.tools



            print(

                "DYNAMIC TOOLS:",

                [

                    tool["function"]["name"]

                    for tool in available_tools

                ],

                flush=True

            )



        except Exception as e:

            print(

                f"TOOL ROUTING ERROR: {e}. Using all tools.",

                flush=True

            )

            available_tools = self.tools





        # Fast path for simple time and date requests.

        normalized_input = user_input.casefold().strip()



        fast_path_tool = None



        if re.search(

            r"\b(what time is it|current time|tell me the time|"

            r"what's the time|what is the time)\b",

            normalized_input

        ):

            fast_path_tool = "get_time"



        elif re.search(

            r"\b(what is today's date|what's today's date|"

            r"what is the date|what's the date|current date|"

            r"today's date|tell me the date)\b",

            normalized_input

        ):

            fast_path_tool = "get_date"



        if fast_path_tool:

            print(

                f"FAST PATH: Executing {fast_path_tool} without LLM",

                flush=True

            )



            tool_start_time = time.perf_counter()



            result = self.registry.execute(

                fast_path_tool,

                {}

            )



            tool_duration = time.perf_counter() - tool_start_time

            tool_timings.append((fast_path_tool, tool_duration))



            if (

                isinstance(result, dict)

                and result.get("success") is True

            ):

                value = result.get("result")



                print(

                    f"FAST PATH RESULT: {value}",

                    flush=True

                )



                print_performance_summary()



                if fast_path_tool == "get_time":

                    return f"It's {value}."



                return f"Today's date is {value}."



            error = (

                result.get("error", "Unknown error.")

                if isinstance(result, dict)

                else "Unexpected tool result."

            )



            print_performance_summary()



            return f"I couldn't retrieve that information: {error}"





        max_tool_steps = 5

        tool_steps = 0



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



        executed_tool_calls = set()

        for _ in range(max_tool_steps + 1):

            llm_start_time = time.perf_counter()



            response = self.llm.chat(

                messages,

                tools=available_tools

            )



            usage = self.llm.last_usage



            llm_token_totals["prompt_tokens"] += usage.get(

                "prompt_tokens", 0

            )

            llm_token_totals["completion_tokens"] += usage.get(

                "completion_tokens", 0

            )

            llm_token_totals["total_tokens"] += usage.get(

                "total_tokens", 0

            )



            llm_duration = time.perf_counter() - llm_start_time

            llm_timings.append(llm_duration)



            print(

                f"LLM CALL TIME: {llm_duration:.3f} sec",

                flush=True

            )



            print("LLM RESPONSE:", response)



            tool_calls = response.get("tool_calls")

            content = response.get("content")

            if tool_calls and tool_steps >= max_tool_steps:

                print(

                    "MAXIMUM TOOL EXECUTION STEPS REACHED",

                    flush=True

                )

                print_performance_summary()

                return (

                    "I couldn't complete the request because "

                    "the maximum number of tool operations was reached."

                )



            # Return a normal final response when available.

            if not tool_calls:

                if isinstance(content, str) and content.strip():

                    print_performance_summary()

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



            # Preserve only the next tool call in the conversation history.

            # This keeps the tool-call message valid while allowing the LLM

            # to inspect the result before choosing the next operation.

            assistant_tool_response = response.copy()

            assistant_tool_response["tool_calls"] = tool_calls

            messages.append(assistant_tool_response)



            # Execute one tool at a time. Any remaining independent or

            # dependent actions can be requested by the LLM on the next turn.

            for tool_call in tool_calls:

                tool_steps += 1

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

                    # If the user explicitly named a browser for this search,

                    # enforce that choice instead of relying only on the LLM.

                    # If no browser was named, search_web uses the default browser.

                    if tool_name == "search_web":

                        browser_match = re.search(

                            r"\b(?:open|launch|start|use|using|in|on|with)\s+"

                            r"(?:the\s+)?"

                            r"(microsoft\s+edge|edge|google\s+chrome|"

                            r"chrome|firefox|brave|opera)\b",

                            user_input,

                            re.IGNORECASE

                        )



                        if browser_match:

                            requested_browser = browser_match.group(1).lower()



                            if requested_browser in ("microsoft edge", "edge"):

                                arguments["browser"] = "edge"

                            elif requested_browser in ("google chrome", "chrome"):

                                arguments["browser"] = "chrome"

                            else:

                                arguments["browser"] = requested_browser

                        # If the utterance does not match the explicit

                        # browser patterns above, preserve any browser value

                        # already supplied by the LLM. Removing it here can

                        # incorrectly force a named-browser request to use

                        # the Windows default browser.





                    # Enforce application launch before typing when explicitly requested.

                    if tool_name == "type_text":



                        app_match = re.search(

                            r"\b(?:open|launch|start|run)\s+(?:the\s+)?"

                            r"(.+?)\s*(?:,?\s*(?:and\s+then|then|and)\s+)"

                            r"(?:type|write|enter)\b",

                            user_input,

                            re.IGNORECASE

                        )



                        if app_match:

                            application = app_match.group(1).strip(" \t.,!?")



                            if application:



                                # Check whether this application was already opened.

                                already_opened = False



                                for executed_name, executed_args in executed_tool_calls:

                                    if executed_name == "open_app":

                                        previous_args = json.loads(executed_args)



                                        if (

                                            previous_args.get("application", "").strip().casefold()

                                            == application.casefold()

                                        ):

                                            already_opened = True

                                            break



                                if not already_opened:

                                    print(

                                        f"PREREQUISITE: Opening {application} before typing",

                                        flush=True

                                    )



                                    open_args = {"application": application}



                                    open_signature = (

                                        "open_app",

                                        json.dumps(open_args, sort_keys=True, default=str)

                                    )



                                    executed_tool_calls.add(open_signature)



                                    open_start = time.perf_counter()



                                    open_result = self.registry.execute(

                                        "open_app",

                                        open_args

                                    )



                                    open_duration = time.perf_counter() - open_start

                                    tool_timings.append(("open_app", open_duration))



                                    print(

                                        "OPEN APP RESULT:",

                                        json.dumps(open_result, indent=2, default=str),

                                        flush=True

                                    )



                                    open_failed = (

                                        isinstance(open_result, dict)

                                        and (

                                            open_result.get("success") is False

                                            or (

                                                isinstance(open_result.get("result"), dict)

                                                and open_result["result"].get("success") is False

                                            )

                                        )

                                    )



                                    if open_failed:

                                        inner = open_result.get("result")

                                        error = (

                                            open_result.get("error")

                                            or (

                                                inner.get("error")

                                                if isinstance(inner, dict)

                                                else None

                                            )

                                            or "Application could not be opened."

                                        )



                                        print_performance_summary()



                                        return (

                                            f"I couldn't type because I couldn't open "

                                            f"{application}: {error}"

                                        )



                    # Prevent the same tool with identical arguments

                    # from being executed more than once per request.

                    call_signature = (

                        tool_name,

                        json.dumps(arguments, sort_keys=True, default=str)

                    )



                    if call_signature in executed_tool_calls:

                        result = {

                            "success": False,

                            "error": (

                                f"Duplicate execution blocked for tool '{tool_name}'."

                            )

                        }



                        print(

                            f"DUPLICATE TOOL CALL BLOCKED: {tool_name}",

                            flush=True

                        )



                    else:

                        executed_tool_calls.add(call_signature)



                        print(

                            f"\nEXECUTING TOOL: {tool_name}",

                            flush=True

                        )

                        print(f"ARGUMENTS: {arguments}", flush=True)



                        tool_start_time = time.perf_counter()



                        result = self.registry.execute(

                            tool_name,

                            arguments

                        )



                        tool_duration = time.perf_counter() - tool_start_time

                        tool_timings.append((tool_name, tool_duration))



                    print(

                        f"TOOL EXECUTION TIME ({tool_name}): "

                        f"{tool_duration:.3f} sec",

                        flush=True

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

                        print_performance_summary()

                        return (

                            "Could not interpret the file search result."

                        )



                    if not search_result.get("success"):

                        print_performance_summary()

                        return (

                            "File search failed: "

                            + search_result.get(

                                "error", "Unknown error."

                            )

                        )



                    matches = search_result.get("matches", [])



                    if not matches:

                        print_performance_summary()

                        return (

                            f"No file matching "

                            f"'{arguments.get('query', '')}' was found."

                        )



                    if len(matches) > 1:

                        print_performance_summary()

                        return (

                            f"Found {len(matches)} matching files. "

                            "Please specify which file you want "

                            "information about:\n"

                            + "\n".join(

                                f"- {match}" for match in matches

                            )

                        )



                    tool_start_time = time.perf_counter()



                    info_result = self.registry.execute(

                        "get_file_info",

                        {"path": matches[0]}

                    )



                    tool_duration = time.perf_counter() - tool_start_time

                    tool_timings.append(("get_file_info", tool_duration))



                    print(

                        f"TOOL EXECUTION TIME (get_file_info): "

                        f"{tool_duration:.3f} sec",

                        flush=True

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

                        print_performance_summary()

                        return formatted



                    print_performance_summary()

                    return (

                        "The file was found, but its metadata "

                        "could not be formatted."

                    )



                if tool_name == "get_file_info":

                    formatted = format_file_info(result)



                    if formatted is not None:

                        print_performance_summary()

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



                    print_performance_summary()

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



        print_performance_summary()

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
