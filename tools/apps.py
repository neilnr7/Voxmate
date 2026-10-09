import json
import subprocess
import win32gui
import win32con
import time



def open_app(application):
    application = application.strip()

    if not application:
        return {
            "success": False,
            "error": "Application name cannot be empty."
        }

    try:
        # First, try to focus an existing application window
        focus_result = focus_app(application)

        if focus_result.get("success"):
            return {
                "success": True,
                "message": f"{application} is already running and has been focused."
            }

        # Get applications registered in the Windows Start Menu
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-StartApps | ConvertTo-Json -Compress"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": "Could not retrieve installed applications."
            }

        apps = json.loads(result.stdout)

        if isinstance(apps, dict):
            apps = [apps]

        application_lower = application.lower()

        # Try exact application name first
        for app in apps:
            name = app.get("Name", "")

            if name.lower() == application_lower:
                app_id = app.get("AppID")

                subprocess.Popen(
                    [
                        "explorer.exe",
                        f"shell:AppsFolder\\{app_id}"
                    ]
                )

                break

        else:
            # Try partial application name
            for app in apps:
                name = app.get("Name", "")

                if application_lower in name.lower():
                    app_id = app.get("AppID")

                    subprocess.Popen(
                        [
                            "explorer.exe",
                            f"shell:AppsFolder\\{app_id}"
                        ]
                    )

                    break

            else:
                # Try applications available through PATH
                path_result = subprocess.run(
                    ["where", application],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if path_result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Could not find application '{application}'."
                    }

                executable = path_result.stdout.strip().splitlines()[0]
                subprocess.Popen([executable])

        # Wait for the application window to appear and focus it
        for _ in range(20):
            time.sleep(0.25)

            focus_result = focus_app(application)

            if focus_result.get("success"):
                return {
                    "success": True,
                    "message": f"{application} opened and focused successfully."
                }

        return {
            "success": False,
            "error": (
                f"{application} was launched, but its window "
                "could not be found or focused."
            )
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not open {application}: {str(e)}"
        }



def close_app(application):
    application = application.strip()

    if not application:
        return {
            "success": False,
            "error": "Application name cannot be empty."
        }

    normalized_application = " ".join(
        application.replace("\u200b", "").split()
    ).lower()

    matched_window = None

    def find_window(hwnd, extra):
        nonlocal matched_window

        if matched_window is not None:
            return

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title:
            return

        normalized_title = " ".join(
            title.replace("\u200b", "").split()
        ).lower()

        if normalized_application in normalized_title:
            matched_window = hwnd

    try:
        # Search all visible top-level windows
        win32gui.EnumWindows(find_window, None)

        if matched_window is None:
            return {
                "success": False,
                "error": f"Application '{application}' is not running."
            }

        # Ask the application to close normally
        win32gui.PostMessage(
            matched_window,
            win32con.WM_CLOSE,
            0,
            0
        )

        return {
            "success": True,
            "message": f"{application} closed successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not close {application}: {str(e)}"
        }


def focus_app(application):
    application = application.strip()

    if not application:
        return {
            "success": False,
            "error": "Application name cannot be empty."
        }

    normalized_application = " ".join(
        application.replace("\u200b", "").split()
    ).lower()

    matched_window = None

    def find_window(hwnd, extra):
        nonlocal matched_window

        if matched_window is not None:
            return

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title:
            return

        normalized_title = " ".join(
            title.replace("\u200b", "").split()
        ).lower()

        if normalized_application in normalized_title:
            matched_window = hwnd

    try:
        # Search all visible top-level windows
        win32gui.EnumWindows(find_window, None)

        if matched_window is None:
            return {
                "success": False,
                "error": f"Application '{application}' is not running."
            }

        # Restore the window if it is minimized
        if win32gui.IsIconic(matched_window):
            win32gui.ShowWindow(
                matched_window,
                win32con.SW_RESTORE
            )

        # Try bringing the requested window to the foreground
        for _ in range(3):
            try:
                win32gui.BringWindowToTop(matched_window)
                win32gui.SetForegroundWindow(matched_window)
            except Exception:
                pass

            time.sleep(0.2)

            if win32gui.GetForegroundWindow() == matched_window:
                return {
                    "success": True,
                    "message": f"{application} focused successfully."
                }

        return {
            "success": False,
            "error": f"Could not bring '{application}' to the foreground."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not focus {application}: {str(e)}"
        }


    

def list_running_apps():
    running_apps = []

    def collect_window(hwnd, extra):
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title.strip():
            return

        running_apps.append(title.strip())

    try:
        # Find all visible top-level application windows
        win32gui.EnumWindows(collect_window, None)

        return {
            "success": True,
            "applications": running_apps
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not list running applications: {str(e)}"
        }
    


OPEN_APP_TOOL = {
    "type": "function",
    "function": {
        "name": "open_app",
        "description": (
            "START or LAUNCH an installed application. "
            "Use this tool only when the user wants to open, start, launch, "
            "or run an application installed on the computer. "
            "Do NOT use this tool when the user is asking to open a website "
            "or web page. "
            "Do NOT use this tool when the user asks to focus, switch to, "
            "activate, or bring an already running application to the foreground."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": "Name of the installed application to start."
                }
            },
            "required": ["application"]
        }
    }
}


CLOSE_APP_TOOL = {
    "type": "function",
    "function": {
        "name": "close_app",
        "description": (
            "CLOSE an application that is currently running. "
            "Use when the user says close, quit, exit, or shut down "
            "an application. Do not open or focus the application."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": "Name of the running application to close."
                }
            },
            "required": ["application"]
        }
    }
}

FOCUS_APP_TOOL = {
    "type": "function",
    "function": {
        "name": "focus_app",
        "description": (
            "Focus an application that is ALREADY OPEN and RUNNING. "
            "Bring its EXISTING window to the foreground. "
            "NEVER open or launch an application with this tool. "
            "Use this tool when the user says: focus, switch to, "
            "activate, bring to front, show, or return to an "
            "already running application."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": (
                        "Name of an application that is already running. "
                        "Example: Notepad, Chrome, Microsoft Edge."
                    )
                }
            },
            "required": ["application"]
        }
    }
}


LIST_RUNNING_APPS_TOOL = {
    "type": "function",
    "function": {
        "name": "list_running_apps",
        "description": (
            "List all currently running applications with visible "
            "windows on the Windows computer."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}