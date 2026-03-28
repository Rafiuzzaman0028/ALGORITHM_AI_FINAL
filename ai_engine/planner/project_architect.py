class ProjectArchitect:
    """
    Determines project structure based on the user goal.
    """

    def generate_structure(self, goal):

        goal = goal.lower()

        if "website" in goal:

            return {
                "project_name": "travel_website",
                "folders": [
                    "frontend",
                    "backend",
                    "docs"
                ]
            }

        if "slides" in goal or "presentation" in goal:

            return {
                "project_name": "presentation_project",
                "folders": [
                    "slides",
                    "research"
                ]
            }

        return {
            "project_name": "general_project",
            "folders": [
                "src",
                "docs"
            ]
        }