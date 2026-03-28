import os
from tavily import TavilyClient


class WebSearchTool:
    """
    Web search tool using Tavily API
    """

    def __init__(self):

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in .env")

        self.client = TavilyClient(api_key=api_key)

    def search(self, query):

        try:

            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=5
            )

            results = []

            for r in response["results"]:

                results.append({
                    "title": r["title"],
                    "url": r["url"],
                    "content": r["content"]
                })

            return {
                "status": "success",
                "result": results
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }