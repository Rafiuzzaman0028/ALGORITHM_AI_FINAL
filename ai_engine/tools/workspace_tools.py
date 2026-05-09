import os
import subprocess


class WorkspaceTools:

    WORKSPACE_ROOT = "generated_projects/active_project"

    def _sanitize_path(self, path):
        """
        Removes redundant root names and prevents directory traversal.
        """
        path = path.strip().replace("\\", "/").strip("/")
        
        # Remove common self-referencing roots that cause nesting
        bad_roots = ["generated_projects", "active_project"]
        path_parts = path.split("/")
        
        filtered_parts: list[str] = [str(p) for p in path_parts if p not in bad_roots and p != ".."]
        
        return os.path.normpath("/".join(filtered_parts))

    def read_file(self, path):
        """Read file content"""
        try:
            path = self._sanitize_path(path)
            full_path = os.path.join(self.WORKSPACE_ROOT, path)

            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            return str(e)

    def write_file(self, input_text):
        """
        Write content to file.
        Expected format: file_path | content
        """

        try:

            if "|" not in input_text:
                return "Invalid input format. Use: file_path | content"

            path, content = input_text.split("|", 1)

            path = self._sanitize_path(path)
            content = content.strip()

            full_path = os.path.join(self.WORKSPACE_ROOT, path)
            full_path = os.path.normpath(full_path)

            folder = os.path.dirname(full_path)
            os.makedirs(folder, exist_ok=True)

            if os.path.exists(full_path):
                return f"File already exists, skipping: {full_path}"

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"File written successfully: {full_path}"

        except Exception as e:
            return str(e)

    def edit_file(self, path, new_content):
        """Overwrite file with new content"""
        try:

            path = os.path.normpath(path)
            full_path = os.path.join(self.WORKSPACE_ROOT, path)
            full_path = os.path.normpath(full_path)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            return "File edited successfully"

        except Exception as e:
            return str(e)

    def list_directory(self, path="."):
        """List files in directory within workspace"""
        try:
            path = self._sanitize_path(path)
            full_path = os.path.join(self.WORKSPACE_ROOT, path)
            
            if not os.path.exists(full_path) or not os.path.isdir(full_path):
                return []
                
            return os.listdir(full_path)

        except Exception as e:
            return str(e)


    def run_terminal(self, command):
        return "Terminal execution disabled."