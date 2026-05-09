from ai_engine.providers.openai_client import OpenAIProvider
from ai_engine.providers.claude_client import ClaudeClient
from ai_engine.providers.gemini_client import GeminiClient
from ai_engine.providers.nvidia_client import NvidiaClient

class ProviderFactory:
    """
    Factory class to return the correct AI provider instance.
    """

    @staticmethod
    def get_provider(provider_name: str):
        provider_name = provider_name.lower()

        if provider_name == "openai":
            return OpenAIProvider()

        elif provider_name == "claude":
            return ClaudeClient()

        elif provider_name == "gemini":
            return GeminiClient()

        elif provider_name == "nvidia":
            return NvidiaClient()


        else:
            raise ValueError(f"Unsupported provider: {provider_name}")