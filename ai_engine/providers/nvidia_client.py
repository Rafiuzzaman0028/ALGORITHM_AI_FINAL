from ai_engine.providers.base_provider import BaseProvider
import requests
import os


class NvidiaClient(BaseProvider):

    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")

    def generate_response(self, prompt, config=None):

        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta/llama3-70b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        data = response.json()

        return {
            "provider": "nvidia",
            "status": "success",
            "output": data["choices"][0]["message"]["content"],
            "tokens_used": None
        }