import json
import subprocess
import win32gui
import win32con


def open_app(application):
    application = application.strip()

    if not application:
        return {
            "success": False,
            "error": "Application name cannot be empty."
        }

    try:
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

                return {
                    "success": True,
                    "message": f"{name} opened successfully."
                }

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

                return {
                    "success": True,
                    "message": f"{name} opened successfully."
                }

        # Try applications available through PATH
        path_result = subprocess.run(
            ["where", application],
            capture_output=True,
            text=True,
            timeout=5
        )

        if path_result.returncode == 0:
            executable = path_result.stdout.strip().splitlines()[0]

            subprocess.Popen([executable])

            return {
                "success": True,
                "message": f"{application} opened successfully."
            }

        return {
            "success": False,
            "error": f"Could not find application '{application}'."
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


OPEN_APP_TOOL = {
    "type": "function",
    "function": {
        "name": "open_app",
        "description": "Open any installed application on the Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": "The name of the application to open."
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
        "description": "Close a running application on the Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": "The name of the application to close."
                }
            },
            "required": ["application"]
        }
    }
}