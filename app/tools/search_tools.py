from ddgs import DDGS
from .registry import registry

def web_search(query: str, max_results: int = 5) -> str:
    """
    Performs a web search using DuckDuckGo and returns the results.
    """
    try:
        results_list = []
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                results_list.append(r)
        
        if not results_list:
            return f"No results found for '{query}'."
        
        formatted_results = []
        for i, r in enumerate(results_list, 1):
            formatted_results.append(f"{i}. {r['title']}\n   URL: {r['href']}\n   Snippet: {r['body']}")
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing search: {str(e)}"

def register_search_tools():
    registry.register(
        name="web_search",
        description="Search the web for information using DuckDuckGo. Useful for finding current events, facts, or general knowledge.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 5).",
                    "default": 5
                }
            },
            "required": ["query"]
        },
        func=web_search
    )
