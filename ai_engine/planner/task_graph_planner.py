from ai_engine.providers.provider_factory import ProviderFactory
import json
import re


class TaskGraphPlanner:
    """
    Creates a multi-step task graph from a user goal.
    This allows the AI to break complex prompts into
    ordered tasks with dependencies.
    """

    def __init__(self):
        self.provider = ProviderFactory.get_provider("openai")

    def create_graph(self, goal):

        prompt = f"""
You are an AI planning system.

Break the following goal into a structured task graph.

Goal:
{goal}

Rules:

1. Identify multiple tasks required.
2. Assign each task an id.
3. Add dependencies if needed.

Return JSON in this format:

{{
 "tasks":[
   {{"id":1,"task":"research topic","depends_on":[]}},
   {{"id":2,"task":"design architecture","depends_on":[1]}},
   {{"id":3,"task":"build backend","depends_on":[2]}}
 ]
}}
"""

        response = self.provider.generate_response(prompt)

        output = response.get("output", "")

        cleaned = re.sub(r"```json|```", "", output).strip()

        try:

            graph = json.loads(cleaned)
            graph["goal"] = goal
            return graph

        except:
            return {"tasks": []}