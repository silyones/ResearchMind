import asyncio

from langchain.tools import tool

from backend.services.tavily_service import search as tavily_search
from backend.utils.logger import get_logger
from backend.utils.search_format import format_search_results

logger = get_logger(__name__)


@tool
def web_search(query: str) -> str:
    """
    Search the web for current information on a topic.

    Args:
        query: The search query string

    Returns:
        Compact search results with title, url, date, and content snippet
    """
    try:
        results = asyncio.run(tavily_search(query))
        formatted = format_search_results(results)
        logger.info(
            f"Web search completed for query: '{query}' - Found {len(results)} results"
        )
        return formatted
    except Exception as e:
        logger.error(f"Error in web_search tool for query '{query}': {str(e)}")
        return "Search failed."
