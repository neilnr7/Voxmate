import pyautogui


def type_text(text):
    pyautogui.write(text, interval=0.02)
    return "Text typed successfully."


def press_key(key):
    pyautogui.press(key)
    return f"Pressed {key}."


def hotkey(keys):
    pyautogui.hotkey(*keys)
    return f"Pressed {'+'.join(keys)}."


def click(x, y):
    pyautogui.click(x, y)
    return f"Clicked at ({x}, {y})."


def scroll(amount):
    pyautogui.scroll(amount)
    return f"Scrolled {amount}."

TYPE_TEXT_TOOL = {
    "type": "function",
    "function": {
        "name": "type_text",
        "description": "Type text using the keyboard into the currently active application.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to type."
                }
            },
            "required": ["text"]
        }
    }
}


PRESS_KEY_TOOL = {
    "type": "function",
    "function": {
        "name": "press_key",
        "description": "Press a single keyboard key.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The key to press, such as enter, escape, tab, or f5."
                }
            },
            "required": ["key"]
        }
    }
}


HOTKEY_TOOL = {
    "type": "function",
    "function": {
        "name": "hotkey",
        "description": "Press multiple keyboard keys together, such as Ctrl+C or Alt+Tab.",
        "parameters": {
            "type": "object",
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Keys to press together."
                }
            },
            "required": ["keys"]
        }
    }
}


CLICK_TOOL = {
    "type": "function",
    "function": {
        "name": "click",
        "description": "Click the mouse at a specific screen coordinate.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "Horizontal screen coordinate."
                },
                "y": {
                    "type": "integer",
                    "description": "Vertical screen coordinate."
                }
            },
            "required": ["x", "y"]
        }
    }
}


SCROLL_TOOL = {
    "type": "function",
    "function": {
        "name": "scroll",
        "description": "Scroll the currently active application. Positive values scroll up; negative values scroll down.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": "Number of scroll units. Positive for up, negative for down."
                }
            },
            "required": ["amount"]
        }
    }
}