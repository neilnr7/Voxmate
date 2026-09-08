import os
from datetime import datetime
import pyautogui


def take_screenshot(filename=None):
    user_home = os.path.expanduser("~")
    one_drive = os.environ.get("OneDrive")

    if one_drive:
        screenshots_folder = os.path.join(
            one_drive,
            "Pictures",
            "Screenshots"
        )
    else:
        screenshots_folder = os.path.join(
            user_home,
            "Pictures",
            "Screenshots"
        )

    os.makedirs(screenshots_folder, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"

    filepath = os.path.join(
        screenshots_folder,
        filename
    )

    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    return f"Screenshot saved as {filepath}."

TAKE_SCREENSHOT_TOOL = {
    "type": "function",
    "function": {
        "name": "take_screenshot",
        "description": (
            "Take a screenshot of the current screen and save it "
            "to the user's Screenshots folder."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}