from ai_engine.providers.provider_factory import ProviderFactory


class TaskAnalyzer:
    """
    Task Analyzer uses AI to analyze user prompts
    and detect one or multiple tasks.
    """

    def __init__(self):
        self.provider = ProviderFactory.get_provider("openai")

    def analyze(self, user_prompt: str):
        """
        Analyze the user prompt and return detected tasks.
        """

        analyzer_prompt = f"""
You are an AI task analyzer.

Your job is to analyze user prompts and identify tasks.

Supported task types:
- conversation
- website
- web_app
- slides
- research
- design
- automation

Rules:
1. Detect if the prompt contains multiple tasks.
2. Assign a task_type to each task.
3. Assign execution priority (1 = first).
4. Return ONLY valid JSON.
5. Do NOT include 'slides' unless the user explicitly asks for a presentation or slides.
6. If the user asks to generate, create, draw, or make an image, picture, photo, cartoon, logo, poster, avatar, or illustration, use task_type "image_generation".

User prompt:
{user_prompt}

Example output:

{{
 "tasks":[
   {{
     "task_type":"website",
     "intent":"build landing page",
     "priority":1
   }}
 ]
}}
"""

        response = self.provider.generate_response(analyzer_prompt)

        return response