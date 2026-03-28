from ai_engine.providers.provider_factory import ProviderFactory


def test_openai():
    prompt = "Explain artificial intelligence in simple terms."

    provider = ProviderFactory.get_provider("openai")

    response = provider.generate_response(prompt)

    print("\n--- AI RESPONSE ---\n")

    print("Provider:", response["provider"])
    print("Status:", response["status"])
    print("Output:", response["output"])
    print("Tokens Used:", response["tokens_used"])


if __name__ == "__main__":
    test_openai()