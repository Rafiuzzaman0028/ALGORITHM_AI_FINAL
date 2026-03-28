from ai_engine.prompts.website_prompt import WEBSITE_PROMPT
from ai_engine.prompts.app_prompt import APP_PROMPT
from ai_engine.prompts.chat_prompt import CHAT_PROMPT
from ai_engine.prompts.design_prompt import DESIGN_PROMPT
from ai_engine.prompts.research_prompt import RESEARCH_PROMPT
from ai_engine.prompts.slides_prompt import SLIDES_PROMPT
from ai_engine.prompts.automation_prompt import AUTOMATION_PROMPT


class PromptManager:

    @staticmethod
    def get_prompt(task_type, user_prompt):

        if task_type == "website":
            return WEBSITE_PROMPT.format(user_prompt=user_prompt)

        elif task_type == "app":
            return APP_PROMPT.format(user_prompt=user_prompt)

        elif task_type == "chat":
            return CHAT_PROMPT.format(user_prompt=user_prompt)

        elif task_type == "design":
            return DESIGN_PROMPT.format(user_prompt=user_prompt)

        elif task_type == "research":
            return RESEARCH_PROMPT.format(user_prompt=user_prompt)

        elif task_type == "slides":
            return SLIDES_PROMPT.format(user_prompt=user_prompt)

        elif task_type in ["automation", "python"]:
            return AUTOMATION_PROMPT.format(user_prompt=user_prompt)

        return user_prompt