class ContextBuilder:

    def build_context(self, user_prompt, document_context=None):

        system_instruction = """
You are Algorithms AI, an autonomous AI agent capable of generating
software projects, automation scripts, reports, and research analysis.
Return structured outputs when generating files.
"""

        context = ""

        if document_context:
            context += f"\nDOCUMENT CONTEXT:\n{document_context}\n"

        final_prompt = f"""
{system_instruction}

{context}

USER REQUEST:
{user_prompt}
"""

        return final_prompt
