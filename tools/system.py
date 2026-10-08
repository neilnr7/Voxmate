from datetime import datetime
import psutil
import subprocess
import wmi
from pycaw.pycaw import AudioUtilities


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


def set_volume(level):
    try:
        level = int(level)

        if level < 0 or level > 100:
            return {
                "success": False,
                "error": "Volume must be between 0 and 100."
            }

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        volume.SetMasterVolumeLevelScalar(
            level / 100.0,
            None
        )

        # Unmute when setting a non-zero volume
        if level > 0 and volume.GetMute():
            volume.SetMute(0, None)

        return {
            "success": True,
            "message": f"Volume set to {level}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Volume must be between 0 and 100."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not set volume: {str(e)}"
        }


def mute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        volume.SetMute(1, None)

        return {
            "success": True,
            "message": "Volume muted successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not mute volume: {str(e)}"
        }


def unmute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        volume.SetMute(0, None)

        return {
            "success": True,
            "message": "Volume unmuted successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not unmute volume: {str(e)}"
        }


def increase_volume(amount=10):
    try:
        amount = int(amount)

        if amount <= 0 or amount > 100:
            return {
                "success": False,
                "error": "Volume increase must be between 1 and 100."
            }

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()
        new_level = min(1.0, current + (amount / 100.0))

        volume.SetMasterVolumeLevelScalar(new_level, None)

        if new_level > 0 and volume.GetMute():
            volume.SetMute(0, None)

        return {
            "success": True,
            "message": f"Volume increased to {round(new_level * 100)}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Volume increase must be a valid number."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not increase volume: {str(e)}"
        }


def decrease_volume(amount=10):
    try:
        amount = int(amount)

        if amount <= 0 or amount > 100:
            return {
                "success": False,
                "error": "Volume decrease must be between 1 and 100."
            }

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()
        new_level = max(0.0, current - (amount / 100.0))

        volume.SetMasterVolumeLevelScalar(new_level, None)

        return {
            "success": True,
            "message": f"Volume decreased to {round(new_level * 100)}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Volume decrease must be a valid number."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not decrease volume: {str(e)}"
        }


#brightness functions
def set_brightness(level):
    try:
        level = int(level)

        if level < 0 or level > 100:
            return {
                "success": False,
                "error": "Brightness must be between 0 and 100."
            }

        brightness = wmi.WMI(namespace="wmi").WmiMonitorBrightnessMethods()

        if not brightness:
            return {
                "success": False,
                "error": "No brightness control is available."
            }

        for monitor in brightness:
            monitor.WmiSetBrightness(level, 0)

        return {
            "success": True,
            "message": f"Brightness set to {level}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Brightness must be between 0 and 100."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not set brightness: {str(e)}"
        }


def increase_brightness(amount=10):
    try:
        amount = int(amount)

        if amount <= 0 or amount > 100:
            return {
                "success": False,
                "error": "Brightness increase must be between 1 and 100."
            }

        brightness = wmi.WMI(namespace="wmi").WmiMonitorBrightness()
        methods = wmi.WMI(namespace="wmi").WmiMonitorBrightnessMethods()

        if not brightness or not methods:
            return {
                "success": False,
                "error": "No brightness control is available."
            }

        current = brightness[0].CurrentBrightness
        new_level = min(100, current + amount)

        for monitor in methods:
            monitor.WmiSetBrightness(new_level, 0)

        return {
            "success": True,
            "message": f"Brightness increased to {new_level}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Brightness increase must be a valid number."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not increase brightness: {str(e)}"
        }


def decrease_brightness(amount=10):
    try:
        amount = int(amount)

        if amount <= 0 or amount > 100:
            return {
                "success": False,
                "error": "Brightness decrease must be between 1 and 100."
            }

        brightness = wmi.WMI(namespace="wmi").WmiMonitorBrightness()
        methods = wmi.WMI(namespace="wmi").WmiMonitorBrightnessMethods()

        if not brightness or not methods:
            return {
                "success": False,
                "error": "No brightness control is available."
            }

        current = brightness[0].CurrentBrightness
        new_level = max(0, current - amount)

        for monitor in methods:
            monitor.WmiSetBrightness(new_level, 0)

        return {
            "success": True,
            "message": f"Brightness decreased to {new_level}%."
        }

    except ValueError:
        return {
            "success": False,
            "error": "Brightness decrease must be a valid number."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not decrease brightness: {str(e)}"
        }

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


SET_VOLUME_TOOL = {
    "type": "function",
    "function": {
        "name": "set_volume",
        "description": (
            "Set the Windows system volume to a specific percentage "
            "from 0 to 100."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "integer",
                    "description": (
                        "The desired system volume percentage, "
                        "from 0 to 100."
                    ),
                    "minimum": 0,
                    "maximum": 100
                }
            },
            "required": ["level"]
        }
    }
}

MUTE_VOLUME_TOOL = {
    "type": "function",
    "function": {
        "name": "mute_volume",
        "description": (
            "Mute the Windows system audio volume."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


UNMUTE_VOLUME_TOOL = {
    "type": "function",
    "function": {
        "name": "unmute_volume",
        "description": (
            "Unmute the Windows system audio volume."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

INCREASE_VOLUME_TOOL = {
    "type": "function",
    "function": {
        "name": "increase_volume",
        "description": (
            "Increase the Windows system volume. "
            "If no amount is specified, increase it by 10 percent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": (
                        "The amount to increase the volume by, "
                        "as a percentage. Defaults to 10."
                    ),
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10
                }
            },
            "required": []
        }
    }
}


DECREASE_VOLUME_TOOL = {
    "type": "function",
    "function": {
        "name": "decrease_volume",
        "description": (
            "Decrease the Windows system volume. "
            "If no amount is specified, decrease it by 10 percent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": (
                        "The amount to decrease the volume by, "
                        "as a percentage. Defaults to 10."
                    ),
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10
                }
            },
            "required": []
        }
    }
}

SET_BRIGHTNESS_TOOL = {
    "type": "function",
    "function": {
        "name": "set_brightness",
        "description": (
            "Set the Windows screen brightness to a specific percentage "
            "from 0 to 100."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "integer",
                    "description": (
                        "The desired screen brightness percentage, "
                        "from 0 to 100."
                    ),
                    "minimum": 0,
                    "maximum": 100
                }
            },
            "required": ["level"]
        }
    }
}


INCREASE_BRIGHTNESS_TOOL = {
    "type": "function",
    "function": {
        "name": "increase_brightness",
        "description": (
            "Increase the Windows screen brightness. "
            "If no amount is specified, increase it by 10 percent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": (
                        "The amount to increase brightness by, "
                        "as a percentage. Defaults to 10."
                    ),
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10
                }
            },
            "required": []
        }
    }
}


DECREASE_BRIGHTNESS_TOOL = {
    "type": "function",
    "function": {
        "name": "decrease_brightness",
        "description": (
            "Decrease the Windows screen brightness. "
            "If no amount is specified, decrease it by 10 percent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": (
                        "The amount to decrease brightness by, "
                        "as a percentage. Defaults to 10."
                    ),
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10
                }
            },
            "required": []
        }
    }
}