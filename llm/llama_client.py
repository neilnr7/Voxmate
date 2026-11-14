
import requests


class LlamaClient:
    def __init__(self, base_url="http://127.0.0.1:8082"):
        self.base_url = base_url.rstrip("/")

        # Store token usage from the latest LLM request.
        self.last_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }

    def chat(self, messages, tools=None):
        payload = {
            "messages": messages,
            "temperature": 0
        }

        if tools:
            payload["tools"] = tools

        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            timeout=120
        )

        if not response.ok:
            print("\nLLM SERVER ERROR")
            print("HTTP status:", response.status_code)
            print("Response body:", response.text)
            response.raise_for_status()

        data = response.json()

        # Capture token usage returned by the LLM server.
        usage = data.get("usage", {})

        self.last_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0)
        }

        return data["choices"][0]["message"]
