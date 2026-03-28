import subprocess
import tempfile
import os


class PythonTool:
    """
    Executes Python code safely inside a sandbox file.
    """

    def execute(self, code: str):

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".py",
                mode="w",
                encoding="utf-8"
            ) as f:

                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True
            )

            os.remove(temp_file)

            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }