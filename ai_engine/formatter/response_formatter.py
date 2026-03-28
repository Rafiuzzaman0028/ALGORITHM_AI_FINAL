class ResponseFormatter:
    """
    Normalizes AI provider responses into a standard structure.
    """

    def format_results(self, execution_results):

        formatted_results = []

        for item in execution_results["results"]:

            task_type = item["task_type"]
            provider = item["provider"]
            result = item["result"]

            formatted = {
                "task_type": task_type,
                "provider": provider,
                "status": result.get("status"),
                "output": result.get("output"),
                "tokens_used": result.get("tokens_used")
            }

            formatted_results.append(formatted)

        return {
            "formatted_results": formatted_results
        }