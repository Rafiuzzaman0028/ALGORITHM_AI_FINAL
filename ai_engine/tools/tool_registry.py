from ai_engine.tools.python_tool import PythonTool
from ai_engine.tools.web_search_tool import WebSearchTool
from ai_engine.tools.workspace_tools import WorkspaceTools

class ToolRegistry:
    """
    Registry for all AI tools.
    Allows the AI agent to discover and execute tools.
    """

    def __init__(self):
        self.tools = {
            "python": PythonTool(),
            "web_search": WebSearchTool()
        }
        self.workspace = WorkspaceTools()
        self.tools["read_file"] = self.workspace.read_file
        self.tools["write_file"] = self.workspace.write_file
        self.tools["edit_file"] = self.workspace.edit_file
        self.tools["list_directory"] = self.workspace.list_directory
        self.tools["run_terminal"] = self.workspace.run_terminal


    def register(self, name, tool):
        """Register a tool"""
        self.tools[name] = tool

    def get_tool(self, name):
        """Retrieve tool by name"""
        return self.tools.get(name)

    def list_tools(self):
        """List all available tools"""
        return list(self.tools.keys())