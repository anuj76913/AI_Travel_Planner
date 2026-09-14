import os
from langchain_core.tools import tool

@tool
def destination_search(query: str) -> str:
    """
    Search the web for travel destinations, attractions, and activities.
    Use this to find specific places, reviews, or current events in a city.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_tavily_api_key_here":
        # Mock mode fallback
        return f"[MOCK TAVILY] Results for '{query}': Found popular attractions matching your query such as Dubai Mall, Burj Khalifa, and local Souks. Highly rated by tourists."
    
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        tavily_tool = TavilySearchResults(max_results=3, tavily_api_key=api_key)
        results = tavily_tool.invoke({"query": query})
        return str(results)
    except Exception as e:
        return f"Error during web search: {e}"
