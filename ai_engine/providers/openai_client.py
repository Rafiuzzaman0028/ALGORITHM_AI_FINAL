import os
from dotenv import load_dotenv
from openai import OpenAI

from ai_engine.providers.base_provider import BaseProvider

load_dotenv()


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider implementation.
    Handles communication with OpenAI models.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, prompt: str, config: dict = None):
        """
        Generate response from OpenAI.

        Args:
            prompt (str): Input prompt
            config (dict): Optional model configuration

        Returns:
            dict: Standardized response
        """

        try:
            model = "gpt-4o-mini"  # Default model

            if config and "model" in config:
                model = config["model"]

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            output_text = response.choices[0].message.content

            return {
                "provider": "openai",
                "status": "success",
                "output": output_text,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }

        except Exception as e:
            return {
                "provider": "openai",
                "status": "error",
                "output": str(e),
                "tokens_used": None,
            }

    def generate_chat_response(self, messages: list, config: dict = None):
        """
        Generate response from OpenAI using a conversation history.

        Args:
            messages (list): List of message dictionaries containing "role" and "content"
            config (dict): Optional model configuration

        Returns:
            dict: Standardized response
        """
        try:
            model = "gpt-4o-mini"  # Default model

            if config and "model" in config:
                model = config["model"]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
            )

            output_text = response.choices[0].message.content

            return {
                "provider": "openai",
                "status": "success",
                "output": output_text,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }

        except Exception as e:
            return {
                "provider": "openai",
                "status": "error",
                "output": str(e),
                "tokens_used": None,
            }