import os
import zipfile
import re
import json
try:
    from ai_engine.project_builder.file_parser import FileParser
except (ImportError, ModuleNotFoundError):
    from .file_parser import FileParser


class SmartProjectBuilder:
    """
    Converts AI output into project files and ZIP archive.
    """

    def __init__(self, output_dir="generated_projects", templates_dir="templates"):
        self.output_dir = output_dir
        self.templates_dir = templates_dir
        os.makedirs(self.output_dir, exist_ok=True)



    def extract_python_code(self, text):

        pattern = r"```[\w]*\n(.*?)```"

        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return matches[0].strip()

        return None

    def parse_file_structure(self, text):

        files = []

        pattern = r'([\w\/\.-]+\.\w+).*?```[\w]*\n(.*?)```'

        matches = re.findall(pattern, text, re.DOTALL)

        for filepath, code in matches:

            filepath = filepath.strip()
            code = code.strip()

            files.append((filepath, code))

        return files


    
    def extract_files(self, formatted_results):

        parser = FileParser()
        files = []

        if "formatted_results" not in formatted_results:
            return []

        for item in formatted_results["formatted_results"]:

            output = item.get("output", "")

            parsed_files = parser.parse_files(output)

            for filename, content in parsed_files.items():
                files.append((filename, content))

        return files

 
    def load_template(self, template_name):
        """Loads template metadata."""
        template_path = os.path.join(self.templates_dir, template_name, "metadata.json")
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                return json.load(f)
        return None

    def create_project_structure(self, files, template_name=None):

        project_name = "python_project"
        for filepath, _ in files:
            ext = filepath.lower().split('.')[-1]
            if ext in ["js", "jsx", "ts", "tsx", "json", "html", "css"]:
                project_name = "nodejs_react_project"
                break

        project_path = os.path.join(self.output_dir, project_name)

        os.makedirs(project_path, exist_ok=True)

        template = self.load_template(template_name) if template_name else None

        for filepath, code in files:

            filepath = filepath.strip()

            # Sanitization (parallel to workspace tools)
            bad_roots = ["generated_projects", "active_project", "python_project", "nodejs_react_project"]
            parts = filepath.replace("\\", "/").split("/")
            filtered_parts: list[str] = [str(p) for p in parts if p not in bad_roots and p != ".."]
            filepath = "/".join(filtered_parts)

            full_path = os.path.join(project_path, filepath)
            full_path = os.path.normpath(full_path)

            folder = os.path.dirname(full_path)
            os.makedirs(folder, exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)

        return project_path


# Create ZIP archive

    def create_zip(self, project_path):

        zip_path = project_path + ".zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for root, dirs, files in os.walk(project_path):
                for file in files:

                    full_path = os.path.join(root, file)

                    arcname = os.path.relpath(full_path, project_path)

                    zipf.write(full_path, arcname)

        return zip_path



    def generate_project(self, formatted_results):

        files = self.extract_files(formatted_results)

        # --- AUTOMATION SCRIPT SUPPORT ---
        if not files:

            for item in formatted_results["formatted_results"]:

                if item["task_type"] == "automation":

                    code = self.extract_python_code(item["output"])

                    if code:

                        project_name = "python_project"
                        project_path = os.path.join(self.output_dir, project_name)

                        os.makedirs(project_path, exist_ok=True)

                        script_path = os.path.join(project_path, "script.py")

                        with open(script_path, "w", encoding="utf-8") as f:
                            f.write(code)

                        zip_path = self.create_zip(project_path)

                        return {
                            "status": "success",
                            "project_path": project_path,
                            "zip_path": zip_path
                        }

            return {
                "status": "no_files_detected"
            }

        # --- NORMAL MULTI-FILE PROJECT ---
        project_path = self.create_project_structure(files)

        zip_path = self.create_zip(project_path)

        return {
            "status": "success",
            "project_path": project_path,
            "zip_path": zip_path
        }        