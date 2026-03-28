import json
import re

class ArchitecturePlanner:

    def plan(self, analyzer_result):

        tasks_json = analyzer_result["output"]
        # Clean markdown code blocks from LLM output
        tasks_json = re.sub(r"```json|```", "", tasks_json).strip()
        
        tasks = json.loads(tasks_json)["tasks"]

        architecture = {
            "project_type": None,
            "frontend": {},
            "backend": {},
            "database": None,
            "features": []
        }


        for task in tasks:

            task_type = task["task_type"]
            intent = task["intent"].lower()

            # ---- AUTOMATION PROJECT ----
            if task_type == "automation":

                architecture["project_type"] = "python_automation"

                architecture["backend"] = {
                    "language": "python",
                    "entry_point": "script.py"
                }

                architecture["features"].append("automation_script")

            # ---- WEBSITE PROJECT ----
            elif task_type == "website":

                architecture["project_type"] = "fullstack_web_app"

                if "react" in intent:
                    architecture["frontend"] = {
                        "framework": "React",
                        "folders": [
                            "client/src/components",
                            "client/src/pages",
                            "client/src/context"
                        ]
                    }

                architecture["backend"] = {
                    "framework": "Express",
                    "folders": [
                        "server/routes",
                        "server/models",
                        "server/middleware"
                    ]
                }

                if "database" in intent or "mongo" in intent:
                    architecture["database"] = "MongoDB"



                architecture["features"].append("api_routes")

        return architecture