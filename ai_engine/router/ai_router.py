import json


class AIRouter:
    """
    Determines which AI provider should execute a task.
    """

    def __init__(self):
        pass

    def build_execution_plan(self, analyzer_result):

        # Convert analyzer output string → JSON
        raw_output = analyzer_result["output"]
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3].strip()
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:-3].strip()
            
        output_data = json.loads(raw_output)

        tasks = output_data["tasks"]

        execution_plan = []

        for task in tasks:

            task_type = task["task_type"]

            provider = self._select_provider(task_type)

            execution_plan.append({
                "provider": provider,
                "task_type": task["task_type"],
                "intent": task["intent"],
                "priority": task["priority"]
            })

        return {
            "execution_plan": execution_plan
        }

    def _select_provider(self, task_type):

        if task_type in ["website", "app"]:
            return "gemini"

        elif task_type in ["research", "image_generation"]:
            return "gemini"

        elif task_type == "slides":
            return "gemini"

        elif task_type == "chat":
            return "openai"

        elif task_type == "design":
            return "openai"

        else:
            return "openai"