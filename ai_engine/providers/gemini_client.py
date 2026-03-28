from ai_engine.providers.base_provider import BaseProvider
import requests
import os


class GeminiClient(BaseProvider):

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def generate_response(self, prompt, config=None):

        #url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(url, json=payload)

        data = response.json()
        print("GEMINI RESPONSE: Successfully received data.")

        if "candidates" not in data:
            return {
                "provider": "gemini",
                "status": "error",
                "output": str(data),
                "tokens_used": None
            }

        return {
            "provider": "gemini",
            "status": "success",
            "output": data["candidates"][0]["content"]["parts"][0]["text"],
            "tokens_used": None
        }
        