import os
import zipfile
import re
import json
import uuid
from datetime import datetime

try:
    from ai_engine.project_builder.file_parser import FileParser
except (ImportError, ModuleNotFoundError):
    from .file_parser import FileParser


class SmartProjectBuilder:
    """
    Converts AI output into project files and ZIP archive.
    Creates a new dynamic project folder every time.
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
            files.append((filepath.strip(), code.strip()))

        return files

    def extract_files(self, formatted_results):

        parser = FileParser()
        files = []

        if "formatted_results" not in formatted_results:
            return []

        for item in formatted_results["formatted_results"]:

            output = item.get("output", "")

            print("\n========== AI OUTPUT ==========")
            print(output)
            print("================================\n")

            parsed_files = parser.parse_files(output)

            print("PARSED FILES:", parsed_files)

            for filename, content in parsed_files.items():
                files.append((filename, content))

        return files

    def load_template(self, template_name):
        template_path = os.path.join(
            self.templates_dir,
            template_name,
            "metadata.json"
        )

        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                return json.load(f)

        return None

    def detect_stack(self, files):
        extensions = set()
        filenames = set()

        for filepath, _ in files:
            clean = filepath.lower().replace("\\", "/")
            filenames.add(os.path.basename(clean))

            if "." in clean:
                extensions.add(clean.split(".")[-1])

        if "package.json" in filenames:
            return "nodejs_project"

        if extensions.intersection({"jsx", "tsx"}):
            return "react_project"

        if "html" in extensions:
            return "html_css_project"

        if extensions.intersection({"js", "ts"}):
            return "nodejs_project"

        if extensions.intersection({"py"}):
            return "python_project"

        return "generic_project"

    def create_dynamic_project_name(self, stack_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = uuid.uuid4().hex[:6]
        return f"{stack_name}_{timestamp}_{short_id}"

    def sanitize_filepath(self, filepath):
        filepath = filepath.strip().replace("\\", "/")

        bad_roots = [
            "generated_projects",
            "active_project",
            "python_project",
            "nodejs_react_project",
            "nodejs_project",
            "react_project",
            "html_css_project",
            "generic_project"
        ]

        parts = filepath.split("/")

        filtered_parts = [
            str(p)
            for p in parts
            if p
            and p not in bad_roots
            and p != ".."
            and not p.startswith(".")
        ]

        return "/".join(filtered_parts)

    def create_project_structure(self, files, template_name=None):
        stack_name = self.detect_stack(files)
        project_name = self.create_dynamic_project_name(stack_name)

        project_path = os.path.abspath(
        os.path.join(self.output_dir, project_name)
        )
        os.makedirs(project_path, exist_ok=False)

        template = self.load_template(template_name) if template_name else None

        for filepath, code in files:
            filepath = self.sanitize_filepath(filepath)

            if not filepath:
                continue

            full_path = os.path.abspath(
            os.path.normpath(os.path.join(project_path, filepath))
            )

            if not full_path.startswith(project_path):
                continue

            folder = os.path.dirname(full_path)
            os.makedirs(folder, exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)

        return project_path

    def create_zip(self, project_path):
        zip_path = project_path + ".zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, project_path)
                    zipf.write(full_path, arcname)

        return zip_path

    def generate_project(self, formatted_results):
        files = self.extract_files(formatted_results)

        # --- AUTOMATION / PYTHON SCRIPT SUPPORT ---
        if not files:
            for item in formatted_results.get("formatted_results", []):
                if item.get("task_type") == "automation":
                    code = self.extract_python_code(item.get("output", ""))

                    if code:
                        stack_name = "python_project"
                        project_name = self.create_dynamic_project_name(stack_name)
                        project_path = os.path.join(self.output_dir, project_name)

                        os.makedirs(project_path, exist_ok=False)

                        script_path = os.path.join(project_path, "script.py")

                        with open(script_path, "w", encoding="utf-8") as f:
                            f.write(code)

                        zip_path = self.create_zip(project_path)

                        return {
                            "status": "success",
                            "project_path": project_path,
                            "zip_path": zip_path,
                            "stack": stack_name
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