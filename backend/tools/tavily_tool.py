import asyncio
from typing import List
from langchain.tools import tool
from backend.services.tavily_service import search as tavily_search
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def web_search(query: str) -> List[dict]:
    """
    Search the web for current information on a topic.
    
    Args:
        query: The search query string
    
    Returns:
        List of search results with title, url, content, and published_date
    """
    try:
        # Run async function synchronously for LangChain compatibility
        results = asyncio.run(tavily_search(query))
        logger.info(f"Web search completed for query: '{query}' - Found {len(results)} results")
        return results
    except Exception as e:
        logger.error(f"Error in web_search tool for query '{query}': {str(e)}")
        return []
