import os
from ai_engine.providers.provider_factory import ProviderFactory


class AIRepairAgent:
    """
    AI Repair Agent
    Responsible for fixing runtime errors in generated Python projects.
    """

    def __init__(self):

        # Use OpenAI provider for repairs
        self.provider = ProviderFactory.get_provider("gemini")

    def repair_runtime_error(self, project_path, traceback_error):

        scripts = self._read_all_scripts(project_path)

        if not scripts:
            return {
                "status": "failed",
                "reason": "No .py files found in project"
            }

        repair_prompt = self._build_repair_prompt(scripts, traceback_error)

        response = self.provider.generate_response(repair_prompt)

        if response.get("status") != "success":

            return {
                "status": "failed",
                "reason": "AI repair generation failed"
            }

        from ai_engine.project_builder.file_parser import FileParser
        parser = FileParser()
        
        fixed_files = parser.parse_files(response["output"])
        
        if not fixed_files:
            # Fallback for single script if format was wrong
            raw_code = self._clean_code(response["output"])
            # try to guess which script it was if only one exists
            if len(scripts) == 1:
                only_script = list(scripts.keys())[0]
                self._write_script(os.path.join(project_path, only_script), raw_code)
                return {"status": "repaired", "message": f"{only_script} updated with AI fix (fallback)"}
                
            return {
                "status": "failed",
                "reason": "AI did not return fixed files in correct format."
            }

        for fname, fcode in fixed_files.items():
            full_path = os.path.join(project_path, fname)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            self._write_script(full_path, fcode)

        return {
            "status": "repaired",
            "message": f"Updated files: {list(fixed_files.keys())}"
        }

    def _clean_code(self, code):

        # Remove markdown code fences
        code = code.replace("```python", "")
        code = code.replace("```", "")

        return code.strip()

    def _read_all_scripts(self, project_path):
        scripts = {}
        for root, _, files in os.walk(project_path):
            if "venv" in root or ".git" in root or "__pycache__" in root: continue
            for f in files:
                if f.endswith(".py"):
                    full_path = os.path.join(root, f)
                    with open(full_path, "r", encoding="utf-8") as file:
                        rel_path = os.path.relpath(full_path, project_path)
                        scripts[rel_path] = file.read()
        return scripts

    def _write_script(self, script_path, code):

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

    def _build_repair_prompt(self, scripts, traceback_error):

        prompt = f"""
You are a senior Python engineer.

The following Python project produced a runtime error.

Your job is to FIX the project. 

Return the FULL correctly fixed file(s) using this exact format:

filename.py
```python
code
```

Do NOT include explanations. ONLY return valid Python code blocks with their filenames above them.

--------------------

ERROR TRACEBACK:

{traceback_error}

--------------------

PROJECT FILES:

"""
        for name, content in scripts.items():
            prompt += f"\n{name}\n```python\n{content}\n```\n"

        prompt += "\nFix the error and return the corrected file(s).\n"
        return prompt