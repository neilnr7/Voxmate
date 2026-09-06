import requests


class LlamaClient:
    def __init__(self, base_url="http://127.0.0.1:8082"):
        self.base_url = base_url.rstrip("/")

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

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]