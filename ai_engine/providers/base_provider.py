from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Base interface for all AI providers.
    Every provider must implement generate_response().
    """

    @abstractmethod
    def generate_response(self, prompt: str, config: dict = None):
        """
        Generate response from the AI provider.

        Args:
            prompt (str): The prompt sent to the model
            config (dict): Optional model configuration

        Returns:
            dict: Standardized response
        """
        pass