import os


class ProjectValidator:

    def __init__(self, project_path):
        self.project_path = project_path

    def validate(self):

        project_type = self.detect_project_type()

        if project_type == "node":
            return self.validate_node_project()

        elif project_type == "python":
            return self.validate_python_project()

        elif project_type == "static":
            return self.validate_static_project()

        return {
            "status": "unknown_project_type",
            "issues": []
        }

    # PROJECT TYPE DETECTION


    def detect_project_type(self):
        if self._exists("package.json"):
            return "node"

        if self._exists("index.html") or self._exists("src/index.html"):
            return "static"

        if self._exists("requirements.txt"):
            return "python"

        return "unknown"

    # NODE VALIDATION

    def validate_node_project(self):
        issues = []

        if not self._exists("package.json") and not self._exists("client/package.json"):
            issues.append("Missing package.json")

        has_entry = any([
            self._exists("server/server.js"),
            self._exists("server/index.js"),
            self._exists("client/src/index.js"),
            self._exists("src/index.js"),
            self._exists("index.js"),
        ])

        if not has_entry:
            issues.append("Missing Node/React entry file")

        return self._build_result(issues)

    # PYTHON VALIDATION

    def validate_python_project(self):

        issues = []

        if not self._exists("requirements.txt"):
            issues.append("Missing requirements.txt")

        # Python project entry points
        has_entry = any([
            self._exists("app.py"),
            self._exists("script.py"),
            self._exists("main.py"),
            self._exists("src/app.py"),
            self._exists("src/script.py"),
            self._exists("src/main.py")
        ])
        if not has_entry:
            issues.append("Missing python entry file (app.py, script.py, or main.py in root or src/)")

        return self._build_result(issues)


    # STATIC WEBSITE VALIDATION


    def validate_static_project(self):

        issues = []

        if not self._exists("index.html"):
            issues.append("Missing index.html")

        return self._build_result(issues)


    # RESULT BUILDER


    def _build_result(self, issues):

        if issues:
            return {
                "status": "failed",
                "issues": issues
            }

        return {
            "status": "success",
            "issues": []
        }

    def _exists(self, path):

        return os.path.exists(os.path.join(self.project_path, path))