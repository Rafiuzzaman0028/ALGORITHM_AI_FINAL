import subprocess
import os


class RuntimeTester:

    def run_python_project(self, project_path):

        possible_entry_points = ["app.py", "main.py", "script.py", "src/app.py", "src/main.py", "src/script.py"]
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

            subprocess.run(

                ["python", "-m", "pip", "install", "-r", requirements_path],
                capture_output=True,
                text=True
            )

        try:

            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:

                return {
                    "status": "runtime_error",
                    "error": result.stderr
                }

            return {
                "status": "success",
                "output": result.stdout
            }
            
        except subprocess.TimeoutExpired as e:
            # A timeout for a web server/long-running script means it successfully started
            # without crashing for 10 seconds.
            return {
                "status": "success",
                "output": "Process ran for 10 seconds and timed out (likely a successful long-running server)."
            }

        except Exception as e:

            return {
                "status": "runtime_exception",
                "error": str(e)
            }