import os
import subprocess
from urllib.parse import urlparse, quote_plus
from html.parser import HTMLParser
import time


def open_url(url: str, browser: str = None) -> str:
    """
    Open a website using its HTTP or HTTPS URL.

    Use this tool when the user wants to visit a website or webpage.
    Do not use this tool to launch a browser application by name.
    Use open_app to launch Chrome, Edge, Firefox, or another browser.

    Args:
        url: HTTP or HTTPS URL of the website to open.
        browser: Optional browser to use when opening the website.
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return f"Invalid URL: {url}"

    if not browser:
        os.startfile(url)
        return f"Opened {url}"

    browser_commands = {
        "chrome": "chrome",
        "google chrome": "chrome",
        "edge": "msedge",
        "microsoft edge": "msedge",
        "firefox": "firefox",
        "brave": "brave"
    }

    browser_name = browser.lower().strip()

    if browser_name not in browser_commands:
        return f"Unsupported browser: {browser}"

    subprocess.Popen(
        ["cmd", "/c", "start", "", browser_commands[browser_name], url]
    )

    return f"Opened {url} in {browser}"


def search_web(query: str, browser: str = None) -> str:
    """
    Search the web for information using Google.

    If a browser is specified, open the Google search in that browser.
    If no browser is specified, use the Windows default browser.

    Args:
        query: Search terms or question to look up online.
        browser: Optional browser to use (Chrome, Edge, Firefox, Brave, or Opera).
                 If omitted, the Windows default browser is used.
    """
    if not query or not query.strip():
        return "Search query cannot be empty."

    url = "https://www.google.com/search?q=" + quote_plus(query.strip())

    if browser:
        browser_commands = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "edge": "msedge",
            "microsoft edge": "msedge",
            "firefox": "firefox",
            "brave": "brave",
            "opera": "opera"
        }

        browser_name = browser.lower().strip()

        if browser_name not in browser_commands:
            return f"Unsupported browser: {browser}"

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                browser_commands[browser_name],
                url
            ]
        )

        time.sleep(3)
        return f"Opened Google search for '{query}' in {browser}."

    os.startfile(url)
    time.sleep(3)

    return (
        f"Opened Google search for '{query}' "
        "in the default browser."
    )


class PageTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript"}:
            self.skip_content = True

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript"}:
            self.skip_content = False

    def handle_data(self, data):
        if not self.skip_content and data.strip():
            self.text.append(data.strip())


def get_page_text(url: str) -> str:
    """
    Retrieve readable text content from a webpage.

    Args:
        url: Complete HTTP or HTTPS URL of the webpage.
    """
    try:
        import urllib.request

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                )
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        parser = PageTextParser()
        parser.feed(html)

        return " ".join(parser.text)

    except Exception as e:
        return f"Failed to get page text: {e}"


def go_back() -> str:
    """
    Navigate back to the previous page in the browser.
    """
    subprocess.Popen(
        ["cmd", "/c", "start", "", "javascript:history.back()"]
    )

    return "Went back"
