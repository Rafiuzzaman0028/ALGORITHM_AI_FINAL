class ToolValidator:
    """
    Validates tool inputs before execution.
    Prevents incorrect formats and tool misuse.
    """

    TOOL_SCHEMAS = {
        "web_search": "query",
        "python": "code",
        "read_file": "file_path",
        "write_file": "file_path | content",
        "edit_file": "file_path | new_content",
        "list_directory": "directory_path",
        "run_terminal": "command"
    }

    def validate(self, tool_name, tool_input):

        if tool_name not in self.TOOL_SCHEMAS:
            return False, f"Unknown tool '{tool_name}'"

        schema = self.TOOL_SCHEMAS[tool_name]

        # Tools requiring pipe format
        if "|" in schema:

            if "|" not in tool_input:
                return False, f"{tool_name} requires format: {schema}"

            parts = tool_input.split("|")

            if len(parts) < 2:
                return False, f"{tool_name} requires two parts: {schema}"

        # Basic validation
        if not tool_input or len(tool_input.strip()) == 0:
            return False, f"{tool_name} input cannot be empty"

        return True, "valid"