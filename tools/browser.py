import os
import subprocess
from urllib.parse import urlparse
from html.parser import HTMLParser
import time


def open_url(url, browser=None):
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

def search_web(query):
    if not query or not query.strip():
        return "Search query cannot be empty."

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    os.startfile(url)
    time.sleep(3)

    return f"Searching for: {query}"


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


def get_page_text(url):
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


def go_back():
    subprocess.Popen(
        ["cmd", "/c", "start", "", "javascript:history.back()"]
    )

    return "Went back"