import os


class ProjectInitializer:

    def create_project(self, structure):

        project_name = structure["project_name"]
        folders = structure["folders"]

        base_path = os.path.join("generated_projects", project_name)

        os.makedirs(base_path, exist_ok=True)

        for folder in folders:
            os.makedirs(os.path.join(base_path, folder), exist_ok=True)

        return base_path