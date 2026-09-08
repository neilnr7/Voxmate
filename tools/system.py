from datetime import datetime
import psutil


def get_time():
    return datetime.now().strftime("%I:%M:%S %p")


def get_date():
    return datetime.now().strftime("%A, %B %d, %Y")


def get_battery():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is unavailable."

    percentage = battery.percent

    if battery.power_plugged:
        status = "charging"
    else:
        status = "not charging"

    return f"{percentage:.0f}% ({status})"

GET_TIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Get the current local time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


GET_DATE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_date",
        "description": "Get today's date.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


GET_BATTERY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_battery",
        "description": "Get the computer's current battery level and charging status.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}