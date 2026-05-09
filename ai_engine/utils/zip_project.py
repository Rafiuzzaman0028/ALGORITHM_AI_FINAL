import shutil
import os


class ProjectZipper:
    """
    Creates a downloadable ZIP archive of generated projects.
    """

    def zip_project(self, project_path):

        try:

            project_path = os.path.normpath(project_path)

            if not os.path.exists(project_path):
                return "Project path does not exist"

            zip_path = project_path + ".zip"

            shutil.make_archive(project_path, 'zip', project_path)

            return zip_path

        except Exception as e:
            return str(e)