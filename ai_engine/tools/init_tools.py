from ai_engine.tools.tool_registry import ToolRegistry
from ai_engine.tools.python_tool import PythonTool
from ai_engine.tools.web_search_tool import WebSearchTool


def initialize_tools():

    registry = ToolRegistry()

    registry.register("python", PythonTool())
    registry.register("web_search", WebSearchTool())

    return registry