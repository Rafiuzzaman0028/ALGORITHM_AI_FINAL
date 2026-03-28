class ToolPlanner:

    def __init__(self, engine):
        self.engine = engine

    def create_plan(self, prompt):

        print("\n--- TOOL PLANNER ---\n")

        planning_prompt = f"""
You are an AI task planner.

User request:
{prompt}

Decide the steps required.

Only respond in JSON format like:

{{
 "steps":[
   {{"tool":"web_search","purpose":"research topic"}},
   {{"tool":"python","purpose":"generate code"}}
 ]
}}
"""

        result = self.engine.analyzer.analyze(planning_prompt)

        try:
            import json
            parsed = json.loads(result["output"])
            return parsed.get("steps", [])
        except:
            return []