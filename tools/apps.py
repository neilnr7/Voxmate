def open_app(application):
    return f"{application} would be opened"


OPEN_APP_TOOL = {
    "type": "function",
    "function": {
        "name": "open_app",
        "description": "Open an application on the Windows computer.",
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