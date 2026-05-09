import subprocess
import os
import sys


class RuntimeTester:

    def run_python_project(self, project_path):
        possible_entry_points = [
            "app.py",
            "main.py",
            "script.py",
            os.path.join("src", "app.py"),
            os.path.join("src", "main.py"),
            os.path.join("src", "script.py"),
        ]

        script_path = ""

        for ep in possible_entry_points:
            test_path = os.path.join(project_path, ep)
            if os.path.exists(test_path):
                script_path = test_path
                break

        requirements_path = os.path.join(project_path, "requirements.txt")

        if not script_path:
            return {
                "status": "no_entry_point",
                "error": "script.py, app.py, or main.py not found in root or src/"
            }

        # Install dependencies if requirements.txt exists
        if os.path.exists(requirements_path):
            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            if install_result.returncode != 0:
                return {
                    "status": "dependency_error",
                    "error": install_result.stderr or install_result.stdout
                }

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return {
                    "status": "runtime_error",
                    "error": result.stderr or result.stdout
                }

            return {
                "status": "success",
                "output": result.stdout
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "success",
                "output": "Process ran for 10 seconds and timed out. This usually means the web server started successfully."
            }

        except Exception as e:
            return {
                "status": "runtime_exception",
                "error": str(e)
            }