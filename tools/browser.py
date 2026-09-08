import os
import subprocess
from urllib.parse import urlparse


BROWSER_PATHS = {
    "chrome": [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ],
    "edge": [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    ],
    "firefox": [
        os.path.expandvars(r"%ProgramFiles%\Mozilla Firefox\firefox.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe"),
    ],
}


def open_browser(browser=None):
    if not browser:
        subprocess.Popen(
            ["cmd", "/c", "start", "", "http://www.google.com"]
        )
        return "Default browser opened"

    browser_commands = {
        "chrome": "chrome",
        "google chrome": "chrome",
        "edge": "msedge",
        "microsoft edge": "msedge",
        "firefox": "firefox"
    }

    browser_name = browser.lower().strip()

    if browser_name not in browser_commands:
        return f"Unsupported browser: {browser}"

    command = browser_commands[browser_name]

    installed = any(
    os.path.exists(path)
    for path in BROWSER_PATHS[browser_name]
    )

    if not installed:
        return f"{browser} is not installed or could not be found."

    subprocess.Popen(
        ["cmd", "/c", "start", "", command]
    )

    return f"{browser} opened"

def open_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return f"Invalid URL: {url}"

    os.startfile(url)

    return f"Opened {url}"

def search_web(query):
    if not query or not query.strip():
        return "Search query cannot be empty."

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    os.startfile(url)

    return f"Searching for: {query}"