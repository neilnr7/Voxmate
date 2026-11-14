
import pyperclip


def read_clipboard() -> str:
    """
    Read and return the current text stored in the Windows clipboard.
    """
    return pyperclip.paste()


def write_clipboard(text: str) -> str:
    """
    Copy the provided text to the Windows clipboard.

    Args:
        text: The text to copy to the clipboard.
    """
    pyperclip.copy(text)
    return "Text copied to clipboard."


def clear_clipboard() -> str:
    """
    Clear the current contents of the Windows clipboard.
    """
    pyperclip.copy("")
    return "Clipboard cleared."


READ_CLIPBOARD_TOOL = {
    "type": "function",
    "function": {
        "name": "read_clipboard",
        "description": (
            "Read and return the actual current text stored in the "
            "Windows clipboard. Use this tool whenever the user asks "
            "what is in the clipboard, what they copied, or asks to "
            "read/check the clipboard."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


WRITE_CLIPBOARD_TOOL = {
    "type": "function",
    "function": {
        "name": "write_clipboard",
        "description": "Copy text to the clipboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to copy to the clipboard."
                }
            },
            "required": ["text"]
        }
    }
}


CLEAR_CLIPBOARD_TOOL = {
    "type": "function",
    "function": {
        "name": "clear_clipboard",
        "description": "Clear the current clipboard contents.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
