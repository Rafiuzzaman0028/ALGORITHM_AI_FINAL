from ai_engine.providers.provider_factory import ProviderFactory
from ai_engine.prompts.prompt_manager import PromptManager
from ai_engine.prompts.prompt_builder import PromptBuilder


class ExecutionManager:

    def __init__(self):
        self.prompt_builder = PromptBuilder()

    def execute(self, execution_plan, architecture):

        results = []

        for task in execution_plan["execution_plan"]:

            provider_name = task["provider"]
            if task["task_type"] == "image_generation":
                provider_name = "gemini"
            intent = task["intent"]

            try:
                provider = ProviderFactory.get_provider(provider_name)

                # base template prompt
                base_prompt = PromptManager.get_prompt(
                    task["task_type"],
                    intent
                )

                # build contextual prompt
                structured_prompt = self.prompt_builder.build_prompt(
                    task,
                    architecture
                )

                # combine prompts
                final_prompt = base_prompt + "\n" + structured_prompt

                response = provider.generate_response(final_prompt)

                if response.get("status") == "error":
                    print(f"[{provider_name.upper()} ERROR] {response.get('output')} - Attempting Fallback...")
                    raise Exception("Provider returned error status.")

            except Exception as e:
                if task["task_type"] == "image_generation":
                    response = {
                        "provider": "gemini",
                        "status": "error",
                        "output": f"Gemini image generation failed: {e}",
                        "tokens_used": None
                    }
                else:
                    print(f"[EXECUTION WARNING] Provider {provider_name} failed: {e}. Falling back to default (OpenAI).")
                    try:
                        fallback_provider = ProviderFactory.get_provider("openai")

                        base_prompt = PromptManager.get_prompt(task["task_type"], intent)
                        structured_prompt = self.prompt_builder.build_prompt(task, architecture)
                        final_prompt = base_prompt + "\n" + structured_prompt

                        response = fallback_provider.generate_response(final_prompt)

                    except Exception as fallback_e:
                        print(f"[EXECUTION ERROR] Fallback also failed: {fallback_e}")
                        response = {
                            "provider": provider_name,
                            "status": "error",
                            "output": f"Primary error: {e}. Fallback error: {fallback_e}",
                            "tokens_used": None
                        }

            results.append({
                "task_type": task["task_type"],
                "provider": provider_name,
                "result": response
            })

        return {
            "results": results
        }