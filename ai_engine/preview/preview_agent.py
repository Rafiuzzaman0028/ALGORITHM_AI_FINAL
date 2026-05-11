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

    def read_package_json(self, folder_path):
        package_json_path = Path(folder_path) / "package.json"

        if not package_json_path.exists():
            return {}

        try:
            return json.loads(package_json_path.read_text(encoding="utf-8"))
        except:
            return {}

    def install_dependencies(self, folder_path):
        folder_path = Path(folder_path)

        package_json = folder_path / "package.json"

        if not package_json.exists():
            return

        node_modules = folder_path / "node_modules"

        if node_modules.exists():
            return

        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"

        print(f"\nInstalling dependencies: {folder_path}\n")

        subprocess.run(
            [npm_cmd, "install"],
            cwd=str(folder_path),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )

    def start_process(self, cmd, cwd, env):
        return subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

    def start_preview(self, project_path):
        try:
            project_path = Path(project_path).resolve()

            if not project_path.exists():
                return {
                    "success": False,
                    "error": "Project path does not exist"
                }

            npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
            python_cmd = "python"

            # =========================================================
            # FRONTEND/BACKEND DETECTION
            # =========================================================

            client_path = None
            server_path = None

            for folder in ["client", "frontend"]:
                path = project_path / folder
                if (path / "package.json").exists():
                    client_path = path
                    break

            for folder in ["server", "backend", "api"]:
                path = project_path / folder
                if (path / "package.json").exists():
                    server_path = path
                    break

            root_package = project_path / "package.json"

            # =========================================================
            # FULLSTACK PROJECT
            # =========================================================

            if client_path:

                frontend_port = self.get_free_port()
                backend_port = self.get_free_port()

                frontend_env = os.environ.copy()
                backend_env = os.environ.copy()

                frontend_env["PORT"] = str(frontend_port)
                backend_env["PORT"] = str(backend_port)

                frontend_env["BROWSER"] = "none"

                # Install dependencies
                self.install_dependencies(project_path)

                if client_path:
                    self.install_dependencies(client_path)

                if server_path:
                    self.install_dependencies(server_path)

                backend_process = None

                # -----------------------------------------------------
                # START BACKEND
                # -----------------------------------------------------

                if server_path:
                    server_package = self.read_package_json(server_path)

                    server_scripts = server_package.get("scripts", {})

                    backend_script = None

                    for script in ["dev", "start"]:
                        if script in server_scripts:
                            backend_script = script
                            break

                    if backend_script:
                        backend_process = self.start_process(
                            [npm_cmd, "run", backend_script],
                            cwd=server_path,
                            env=backend_env
                        )

                # -----------------------------------------------------
                # START FRONTEND
                # -----------------------------------------------------

                client_package = self.read_package_json(client_path)

                client_scripts = client_package.get("scripts", {})

                frontend_script = None

                for script in ["dev", "start"]:
                    if script in client_scripts:
                        frontend_script = script
                        break

                if not frontend_script:
                    return {
                        "success": False,
                        "error": "No frontend script found"
                    }

                frontend_process = self.start_process(
                    [npm_cmd, "run", frontend_script],
                    cwd=client_path,
                    env=frontend_env
                )

                time.sleep(8)

                if frontend_process.poll() is not None:
                    stdout, stderr = frontend_process.communicate()

                    return {
                        "success": False,
                        "error": "Frontend failed to start",
                        "stdout": stdout,
                        "stderr": stderr
                    }

                preview_url = f"http://127.0.0.1:{frontend_port}"

                self.active_processes[str(project_path)] = {
                    "frontend": frontend_process,
                    "backend": backend_process,
                    "url": preview_url,
                    "frontend_port": frontend_port,
                    "backend_port": backend_port
                }

                return {
                    "success": True,
                    "url": preview_url,
                    "frontend_port": frontend_port,
                    "backend_port": backend_port,
                    "project_type": "fullstack"
                }

            # =========================================================
            # ROOT NODE PROJECT
            # =========================================================

            elif root_package.exists():

                env = os.environ.copy()

                port = self.get_free_port()

                env["PORT"] = str(port)

                self.install_dependencies(project_path)

                package = self.read_package_json(project_path)

                scripts = package.get("scripts", {})

                script_name = None

                for script in ["dev", "start"]:
                    if script in scripts:
                        script_name = script
                        break

                if not script_name:
                    return {
                        "success": False,
                        "error": "No runnable npm script found"
                    }

                process = self.start_process(
                    [npm_cmd, "run", script_name],
                    cwd=project_path,
                    env=env
                )

                time.sleep(5)

                if process.poll() is not None:
                    stdout, stderr = process.communicate()

                    return {
                        "success": False,
                        "error": "Node project failed to start",
                        "stdout": stdout,
                        "stderr": stderr
                    }

                preview_url = f"http://127.0.0.1:{port}"

                self.active_processes[str(project_path)] = {
                    "frontend": process,
                    "url": preview_url,
                    "frontend_port": port
                }

                return {
                    "success": True,
                    "url": preview_url,
                    "project_type": "node"
                }

            # =========================================================
            # HTML PROJECT
            # =========================================================

            index_html = project_path / "index.html"

            if index_html.exists():

                port = self.get_free_port()

                process = self.start_process(
                    [
                        python_cmd,
                        "-m",
                        "http.server",
                        str(port),
                        "--bind",
                        "127.0.0.1"
                    ],
                    cwd=project_path,
                    env=os.environ.copy()
                )

                preview_url = f"http://127.0.0.1:{port}"

                self.active_processes[str(project_path)] = {
                    "frontend": process,
                    "url": preview_url,
                    "frontend_port": port
                }

                return {
                    "success": True,
                    "url": preview_url,
                    "project_type": "html"
                }

            # =========================================================
            # PYTHON PROJECT
            # =========================================================

            for py_file in ["app.py", "main.py", "server.py", "script.py"]:

                py_path = project_path / py_file

                if py_path.exists():

                    process = self.start_process(
                        [python_cmd, str(py_path)],
                        cwd=project_path,
                        env=os.environ.copy()
                    )

                    time.sleep(3)

                    preview_url = "http://127.0.0.1:5000"

                    self.active_processes[str(project_path)] = {
                        "frontend": process,
                        "url": preview_url
                    }

                    return {
                        "success": True,
                        "url": preview_url,
                        "project_type": "python"
                    }

            return {
                "success": False,
                "error": "Unsupported project type"
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }

    def stop_preview(self, project_path=None, port=None):
        try:
            target_key = None

            # 1. Prefer stopping by project path
            if project_path:
                resolved_path = str(Path(project_path).resolve())

                if resolved_path in self.active_processes:
                    target_key = resolved_path

            # 2. Fallback: stop by frontend/backend port
            if not target_key and port:
                port = int(port)

                for key, process_info in self.active_processes.items():
                    if (
                        process_info.get("frontend_port") == port
                        or process_info.get("backend_port") == port
                        or process_info.get("port") == port
                    ):
                        target_key = key
                        break

            if not target_key:
                return {
                    "success": False,
                    "error": "No active preview found for this project_path or port"
                }

            process_info = self.active_processes[target_key]

            stopped = []

            for process_name in ["frontend", "backend", "process"]:
                process = process_info.get(process_name)

                if process:
                    try:
                        process.terminate()

                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()

                        stopped.append(process_name)

                    except Exception as exc:
                        stopped.append(f"{process_name} stop error: {exc}")

            del self.active_processes[target_key]

            return {
                "success": True,
                "message": "Preview stopped successfully",
                "stopped": stopped,
                "project_path": target_key
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }