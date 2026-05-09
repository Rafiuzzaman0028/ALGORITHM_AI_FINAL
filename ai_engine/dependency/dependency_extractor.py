import os
import re


class DependencyExtractor:

    def extract(self, project_path):

        dependencies = set()

        for root, dirs, files in os.walk(project_path):

            for file in files:

                if file.endswith(".py"):

                    file_path = os.path.join(root, file)

                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    imports = re.findall(
                        r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)",
                        content,
                        re.MULTILINE,
                    )

                    for imp in imports:

                        stdlib = [
                            "os","sys","re","json","math","time","csv","collections",
                            "statistics","typing","pathlib","datetime","argparse",
                            "itertools","functools","subprocess","threading","asyncio"
                        ]

                        if imp not in stdlib:
                            dependencies.add(imp)

        return sorted(dependencies)

    def generate_requirements(self, project_path):

        deps = self.extract(project_path)

        if not deps:
            return

        req_file = os.path.join(project_path, "requirements.txt")

        with open(req_file, "w") as f:

            for dep in deps:
                f.write(dep + "\n")    