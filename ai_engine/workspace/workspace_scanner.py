import os


class WorkspaceScanner:
    """
    Scans the project workspace and returns file structure.
    This allows the agent to know what files already exist.
    """

    def __init__(self, root_path="generated_projects/active_project"):
        self.root_path = root_path


    def scan(self):

        workspace_files = []

        if not os.path.exists(self.root_path):
            return []

        for root, dirs, files in os.walk(self.root_path):

            for file in files:

                full_path = os.path.join(root, file)

                # Ensure we return paths relative to the ACTIVE PROJECT root, not the workspace root
                relative_path = os.path.relpath(full_path, self.root_path)
                
                # Normalize separators and strip dots
                relative_path = os.path.normpath(relative_path).replace("\\", "/")

                workspace_files.append(relative_path)

        return workspace_files