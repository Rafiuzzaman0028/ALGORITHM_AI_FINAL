import os
from ai_engine.providers.provider_factory import ProviderFactory
from ai_engine.repair.runtime_tester import RuntimeTester

class ProjectRepairer:

    def __init__(self):

        self.provider = ProviderFactory.get_provider("gemini")

    def repair(self, project_path, issues):

        print("\n--- AUTO REPAIR STARTED ---\n")
        print("Detected issues:", issues)
        for issue in issues:

            filename = self.detect_missing_file(issue)
            
            if filename:

                print(f"Generating missing file: {filename}")

                code = self.generate_file_code(filename)

                self.create_file(project_path, filename, code)

        print("\n--- AUTO REPAIR COMPLETE ---\n")

        # Runtime Test After Repair


        tester = RuntimeTester()

        runtime_result = tester.run_python_project(project_path)

        print("\n--- RUNTIME TEST AFTER REPAIR ---\n")
        print(runtime_result)



    def detect_missing_file(self, issue):

        prompt = f"""
Analyze this project validation issue and determine the exactly missing or problematic file path.

Issue: {issue}

Return strictly the file path (e.g., client/src/index.js or main.py).
Do not include any other text or explanation.
If you aren't sure which specific file is missing, return NONE.
"""
        try:
            response = self.provider.generate_response(prompt)
            if response.get("status") == "success":
                filename = response.get("output", "").strip()
                if filename and filename.upper() != "NONE":
                    return filename
        except Exception as e:
            print(f"Error detecting missing file: {e}")

        return None



    def generate_file_code(self, filename):

        prompt = f"""
    Generate complete code for the following file:

    {filename}

    Return ONLY the code content without explanation.
    """

        response = self.provider.generate_response(prompt)

        return response["output"]


    def create_file(self, project_path, filename, code):
        full_path = os.path.join(project_path, filename)

        basename = os.path.basename(full_path)

        # FIX: treat paths without extensions as folders
        if "." not in basename:
            os.makedirs(full_path, exist_ok=True)
            return

        # FIX: do not overwrite directories
        if os.path.isdir(full_path):
            return

        folder = os.path.dirname(full_path)
        os.makedirs(folder, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code)