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
    def __init__(self, output_dir="generated_projects", templates_dir="templates"):
        self.output_dir = output_dir
        self.templates_dir = templates_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_python_code(self, text):
        pattern = r"```[\w]*\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0].strip() if matches else None

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

    def detect_stack(self, files):
        extensions = set()

        for filepath, _ in files:
            clean = filepath.lower().replace("\\", "/")

            if "." in clean:
                extensions.add(clean.split(".")[-1])

        if extensions.intersection({"jsx", "tsx"}):
            return "react_project"

        if "html" in extensions:
            return "html_css_project"

        if extensions.intersection({"js", "ts"}):
            return "frontend_project"

        return "frontend_project"

    def create_dynamic_project_name(self, stack_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = uuid.uuid4().hex[:6]
        return f"{stack_name}_{timestamp}_{short_id}"

    def sanitize_filepath(self, filepath):
        filepath = filepath.strip().replace("\\", "/")

        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in filepath for char in invalid_chars):
            return ""

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

    def is_backend_file(self, filepath):
        path = filepath.lower().replace("\\", "/")

        blocked_prefixes = [
            "server/",
            "backend/",
            "api/",
            "routes/",
            "controllers/",
            "models/",
            "middleware/",
            "database/",
            "db/",
            "config/db",
            "config/database"
        ]

        blocked_exact = [
            "server.js",
            "backend.js",
            "database.js",
            "db.js"
        ]

        if any(path.startswith(prefix) for prefix in blocked_prefixes):
            return True

        filename = os.path.basename(path)

        if filename in blocked_exact:
            return True

        return False

    def clean_package_json(self, code):
        """
        Keeps package.json frontend-only.
        Also makes sure React projects include react-scripts
        if the start command uses react-scripts.
        """

        try:
            data = json.loads(code)

            data.setdefault("dependencies", {})
            data.setdefault("devDependencies", {})

            backend_deps = [
                "express",
                "mongoose",
                "mongodb",
                "jsonwebtoken",
                "bcrypt",
                "bcryptjs",
                "cors",
                "dotenv",
                "nodemon"
            ]

            for section in ["dependencies", "devDependencies"]:
                for dep in backend_deps:
                    data.get(section, {}).pop(dep, None)

            all_text = json.dumps(data).lower()

            is_vite = "vite" in all_text
            is_react = (
                "react" in all_text
                or "jsx" in all_text
                or "tsx" in all_text
                or "react-scripts" in all_text
            )

            if is_vite:
                data["dependencies"].setdefault("react", "^18.2.0")
                data["dependencies"].setdefault("react-dom", "^18.2.0")
                data["devDependencies"].setdefault("vite", "^5.0.0")
                data["devDependencies"].setdefault("@vitejs/plugin-react", "^4.2.0")

                data["scripts"] = {
                    "dev": "vite --host 127.0.0.1",
                    "start": "vite --host 127.0.0.1",
                    "build": "vite build",
                    "preview": "vite preview --host 127.0.0.1"
                }

            elif is_react:
                data["dependencies"].setdefault("react", "^18.2.0")
                data["dependencies"].setdefault("react-dom", "^18.2.0")
                data["dependencies"].setdefault("react-scripts", "5.0.1")

                data["scripts"] = {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                }

            else:
                scripts = data.get("scripts", {})
                cleaned_scripts = {}

                for key, value in scripts.items():
                    value_lower = str(value).lower()

                    if any(word in value_lower for word in ["server", "backend", "nodemon", "express"]):
                        continue

                    cleaned_scripts[key] = value

                if cleaned_scripts:
                    data["scripts"] = cleaned_scripts

            if not data["dependencies"]:
                data.pop("dependencies", None)

            if not data["devDependencies"]:
                data.pop("devDependencies", None)

            return json.dumps(data, indent=2)

        except Exception:
            return code

    def create_project_structure(self, files, template_name=None):
        frontend_files = []

        for filepath, code in files:
            filepath = self.sanitize_filepath(filepath)

            if not filepath:
                continue

            if self.is_backend_file(filepath):
                continue

            if filepath.lower().endswith("package.json"):
                code = self.clean_package_json(code)

            frontend_files.append((filepath, code))

        stack_name = self.detect_stack(frontend_files)
        project_name = self.create_dynamic_project_name(stack_name)

        project_path = os.path.abspath(os.path.join(self.output_dir, project_name))
        os.makedirs(project_path, exist_ok=False)

        for filepath, code in frontend_files:
            full_path = os.path.abspath(
                os.path.normpath(os.path.join(project_path, filepath))
            )

            if not full_path.startswith(project_path):
                continue

            basename = os.path.basename(full_path)

            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            if any(char in basename for char in invalid_chars):
                continue

            if "." not in basename:
                os.makedirs(full_path, exist_ok=True)
                continue

            if os.path.isdir(full_path):
                continue

            folder = os.path.dirname(full_path)
            os.makedirs(folder, exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code or "")

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

        if not files:
            return {
                "status": "no_files_detected"
            }

        project_path = self.create_project_structure(files)
        zip_path = self.create_zip(project_path)

        return {
            "status": "success",
            "project_path": project_path,
            "zip_path": zip_path,
            "stack": "frontend_only"
        }