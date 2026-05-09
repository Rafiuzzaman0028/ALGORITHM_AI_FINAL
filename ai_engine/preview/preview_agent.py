import json
import os
import socket
import subprocess
import time
from pathlib import Path


class PreviewAgent:
    def __init__(self):
        self.active_processes = {}

    def get_free_port(self):
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def read_package_json(self, project_path):
        package_json_path = Path(project_path) / "package.json"

        if not package_json_path.exists():
            raise RuntimeError("package.json not found")

        try:
            return json.loads(package_json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Could not read package.json: {exc}") from exc

    def choose_npm_script(self, package_json, package_json_path=None):
        scripts = package_json.get("scripts") or {}

        # Prefer start for preview because it usually uses plain node.
        for script_name in ("start", "serve", "preview"):
            if script_name in scripts:
                return script_name

        # Use dev only if no better option exists.
        if "dev" in scripts:
            dev_script = scripts["dev"]

            # If dev uses nodemon, replace it with node so preview works without nodemon.
            if "nodemon" in dev_script:
                scripts["dev"] = dev_script.replace("nodemon", "node")

                if package_json_path:
                    package_json_path.write_text(
                        json.dumps(package_json, indent=2),
                        encoding="utf-8"
                    )

            return "dev"

        available = ", ".join(sorted(scripts.keys())) or "none"
        raise RuntimeError(
            f"No preview script found in package.json. Available scripts: {available}"
        )

    def install_node_dependencies(self, project_path, npm_cmd, env, script_name):
        """
        Install npm dependencies if node_modules is missing.
        This fixes errors like: Cannot find module 'express'.
        """

        node_modules_path = Path(project_path) / "node_modules"

        if node_modules_path.exists():
            return {
                "success": True,
                "skipped": True,
                "message": "node_modules already exists"
            }

        install_process = subprocess.run(
            [npm_cmd, "install"],
            cwd=str(project_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=180
        )

        if install_process.returncode != 0:
            return {
                "success": False,
                "error": "npm install failed",
                "stdout": install_process.stdout,
                "stderr": install_process.stderr,
                "project_type": "node",
                "script_used": script_name
            }

        return {
            "success": True,
            "skipped": False,
            "message": "npm install completed"
        }

    def find_index_html(self, project_path):
        project_path = Path(project_path)

        direct_index = project_path / "index.html"
        if direct_index.exists():
            return direct_index

        matches = list(project_path.rglob("index.html"))
        if matches:
            return matches[0]

        return None

    def find_python_entry(self, project_path):
        project_path = Path(project_path)

        preferred = [
            "app.py",
            "main.py",
            "server.py",
            "script.py"
        ]

        for name in preferred:
            file_path = project_path / name
            if file_path.exists():
                return file_path

        matches = list(project_path.rglob("*.py"))
        if matches:
            return matches[0]

        return None

    def start_preview(self, project_path):
        try:
            project_path = Path(project_path).resolve()

            if not project_path.exists():
                return {
                    "success": False,
                    "error": "Project path does not exist"
                }

            env = os.environ.copy()
            port = self.get_free_port()
            env["PORT"] = str(port)
            env.setdefault("HOST", "127.0.0.1")

            npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
            python_cmd = "python"

            package_json_path = project_path / "package.json"

            # 1. Node / React / Vite / Express project
            if package_json_path.exists():
                try:
                    package_json = self.read_package_json(project_path)
                    script_name = self.choose_npm_script(package_json, package_json_path)
                except RuntimeError as exc:
                    return {
                        "success": False,
                        "error": str(exc)
                    }

                install_result = self.install_node_dependencies(
                    project_path=project_path,
                    npm_cmd=npm_cmd,
                    env=env,
                    script_name=script_name
                )

                if not install_result.get("success"):
                    return install_result

                cmd = [
                    npm_cmd,
                    "run",
                    script_name
                ]

                cwd = project_path
                project_type = "node"
                script_used = script_name

            else:
                index_html = self.find_index_html(project_path)

                # 2. Plain HTML/CSS/JS project
                if index_html:
                    cwd = index_html.parent

                    cmd = [
                        python_cmd,
                        "-m",
                        "http.server",
                        str(port),
                        "--bind",
                        "127.0.0.1"
                    ]

                    project_type = "html"
                    script_used = "python -m http.server"

                else:
                    python_entry = self.find_python_entry(project_path)

                    # 3. Python project
                    if python_entry:
                        cwd = python_entry.parent

                        cmd = [
                            python_cmd,
                            str(python_entry)
                        ]

                        project_type = "python"
                        script_used = python_entry.name

                    else:
                        return {
                            "success": False,
                            "error": "Unsupported project type. No package.json, index.html, or Python entry file found."
                        }

            process = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

            time.sleep(3)

            if process.poll() is not None:
                stdout, stderr = process.communicate()

                return {
                    "success": False,
                    "error": "Preview server failed to start",
                    "stdout": stdout,
                    "stderr": stderr,
                    "project_type": project_type,
                    "script_used": script_used
                }

            preview_url = f"http://127.0.0.1:{port}"

            self.active_processes[str(project_path)] = {
                "process": process,
                "port": port,
                "url": preview_url,
                "project_type": project_type,
                "script_used": script_used
            }

            return {
                "success": True,
                "url": preview_url,
                "port": port,
                "project_type": project_type,
                "script_used": script_used
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Dependency installation timed out"
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }

    def stop_preview(self, project_path):
        try:
            project_path = str(Path(project_path).resolve())

            if project_path not in self.active_processes:
                return {
                    "success": False,
                    "error": "No active preview found"
                }

            process_info = self.active_processes[project_path]
            process = process_info["process"]

            process.terminate()

            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            del self.active_processes[project_path]

            return {
                "success": True,
                "message": "Preview stopped successfully"
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }

    def get_preview_status(self, project_path):
        try:
            project_path = str(Path(project_path).resolve())

            if project_path not in self.active_processes:
                return {
                    "success": False,
                    "status": "not_running"
                }

            process_info = self.active_processes[project_path]
            process = process_info["process"]

            if process.poll() is not None:
                del self.active_processes[project_path]

                return {
                    "success": False,
                    "status": "stopped"
                }

            return {
                "success": True,
                "status": "running",
                "url": process_info["url"],
                "port": process_info["port"],
                "project_type": process_info.get("project_type"),
                "script_used": process_info.get("script_used")
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }