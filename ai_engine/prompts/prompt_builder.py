class PromptBuilder:

    def build_prompt(self, task, architecture):

        intent = task["intent"]
        task_type = task["task_type"]

        project_type = architecture.get("project_type", "software_project")

        if task_type in ["research", "document", "slides", "text"]:
            prompt = f"""
You are an expert AI assistant.

Task:
{intent}

Task Type:
{task_type}

Rules:
- Provide high quality, engaging textual content.
- DO NOT output code, file paths, or project structures.
- Use markdown formatting appropriately.
- Be highly detailed and comprehensive.
"""
            return prompt

        prompt = f"""
You are a senior software engineer.

Task:
{intent}

Project Type:
{project_type}

Task Type:
{task_type}

Architecture:
{architecture}

Rules:
- Produce production ready code
- Avoid explanations unless necessary
- Use best coding practices
- Include imports
- Write clean readable code
- Use real, meaningful directory names (e.g., src/, app/, config/). Do NOT use placeholder folders like "path/to/".

Output format:

src/main_file.ext
```code_language
# code here
```

requirements.txt
```text
# dependencies here
```

README.md
```markdown
# documentation here
```
"""

        return prompt