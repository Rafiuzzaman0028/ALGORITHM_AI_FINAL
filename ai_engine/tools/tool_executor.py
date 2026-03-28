class ToolExecutor:
    """
    Executes tools requested by the AI agent.
    """

    def __init__(self, tool_registry):
        self.tool_registry = tool_registry

    def execute_tool(self, tool_name, tool_input):

        tool = self.tool_registry.get_tool(tool_name)

        if not tool:
            return {
                "status": "error",
                "error": f"Tool '{tool_name}' not found"
            }

        try:

            # python tool
            if tool_name == "python":
                return tool.execute(tool_input)

            # web search tool
            if tool_name == "web_search":
                return tool.search(tool_input)

            return {
                "status": "error",
                "error": "Unsupported tool"
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }