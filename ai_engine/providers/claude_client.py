from ai_engine.providers.base_provider import BaseProvider
import requests
import os


class ClaudeClient(BaseProvider):

    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")

    def generate_response(self, prompt, config=None):

        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, json=payload, headers=headers)


        data = response.json()

        print("CLAUDE RESPONSE:", data)

        if "content" not in data:
            return {
                "provider": "claude",
                "status": "error",
                "output": str(data),
                "tokens_used": None
            }

        return {
            "provider": "claude",
            "status": "success",
            "output": data["content"][0]["text"],
            "tokens_used": None
        }