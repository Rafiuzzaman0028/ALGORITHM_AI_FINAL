from ai_engine.tools.tool_registry import ToolRegistry


class ResearchAgent:

    def __init__(self):
        self.registry = ToolRegistry()

    def research(self, query):

        tool = self.registry.get_tool("web_search")

        if not tool:
            #return ""
            return []

        result = tool.search(query)

        if result["status"] != "success":
            return []

        sources = result["result"]

        return sources

