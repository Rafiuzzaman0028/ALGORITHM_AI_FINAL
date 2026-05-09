import json


class AIRouter:
    """
    Builds an execution plan from the task analyzer output.
    """

    def build_execution_plan(self, analyzer_result):
        output_data = self._normalize_analyzer_result(analyzer_result)

        tasks = output_data.get("tasks", [])

        execution_plan = []

        for task in tasks:
            task_type = str(task.get("task_type", "chat")).lower().strip()

            execution_plan.append({
                "provider": self._select_provider(task_type),
                "task_type": task_type,
                "intent": task.get("intent", ""),
                "priority": task.get("priority", 1)
            })

        return {
            "execution_plan": execution_plan
        }

    def _normalize_analyzer_result(self, analyzer_result):
        """
        The analyzer may return:
        1. {"tasks": [...]}
        2. {"provider": "...", "status": "success", "output": "{...json...}"}
        3. A raw JSON string

        This method converts all of those into:
        {"tasks": [...]}
        """

        if analyzer_result is None:
            return {"tasks": []}

        # Case 1: provider wrapper with output JSON string
        if isinstance(analyzer_result, dict) and "output" in analyzer_result:
            raw_output = analyzer_result.get("output", "")

            if not isinstance(raw_output, str):
                return {"tasks": []}

            raw_output = raw_output.strip()

            if raw_output.startswith("```json"):
                raw_output = raw_output[7:].strip()

            if raw_output.startswith("```"):
                raw_output = raw_output[3:].strip()

            if raw_output.endswith("```"):
                raw_output = raw_output[:-3].strip()

            try:
                return json.loads(raw_output)
            except Exception as e:
                print("[AIRouter] Failed to parse analyzer output:", e)
                print("[AIRouter] Raw analyzer output:", raw_output)
                return {"tasks": []}

        # Case 2: already parsed dictionary
        if isinstance(analyzer_result, dict):
            return analyzer_result

        # Case 3: raw JSON string
        if isinstance(analyzer_result, str):
            raw_output = analyzer_result.strip()

            if raw_output.startswith("```json"):
                raw_output = raw_output[7:].strip()

            if raw_output.startswith("```"):
                raw_output = raw_output[3:].strip()

            if raw_output.endswith("```"):
                raw_output = raw_output[:-3].strip()

            try:
                return json.loads(raw_output)
            except Exception as e:
                print("[AIRouter] Failed to parse analyzer string:", e)
                return {"tasks": []}

        return {"tasks": []}

    def _select_provider(self, task_type):
        task_type = str(task_type).lower().strip()

        if task_type in ["website", "web_app", "frontend", "html_css", "app"]:
            return "claude"

        if task_type in ["research", "slides", "image_generation"]:
            return "gemini"

        if task_type in ["chat", "design", "python", "automation", "script"]:
            return "openai"

        return "claude"