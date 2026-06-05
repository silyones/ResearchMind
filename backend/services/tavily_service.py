import asyncio
from typing import List, Dict, Any, Set
from tavily import TavilyClient
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Tavily client
client = TavilyClient(api_key=settings.tavily_api_key)


async def search(query: str) -> List[Dict[str, Any]]:
    """
    Search the web for information on a given query using Tavily API.
    
    Args:
        query: The search query string
    
    Returns:
        List of search results with title, url, content, and published_date
    
    Raises:
        Exception: If the search fails
    """
    try:
        logger.info(f"Starting Tavily search for query: '{query}'")
        
        # Run Tavily search in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.search(
                query=query,
                max_results=settings.max_search_results,
                include_answer=True
            )
        )
        
        # Parse and format results
        results = []
        if response and "results" in response:
            for result in response["results"]:
                formatted_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "published_date": result.get("published_date", None)
                }
                results.append(formatted_result)
            
            logger.info(f"Tavily search completed for '{query}' - Retrieved {len(results)} results")
        else:
            logger.warning(f"No results found for query: '{query}'")
        
        return results
    
    except Exception as e:
        logger.error(f"Tavily search error for query '{query}': {str(e)}")
        raise


async def search_multiple(queries: List[str]) -> List[Dict[str, Any]]:
    """
    Execute multiple searches and deduplicate results by URL.
    
    Args:
        queries: List of search query strings
    
    Returns:
        Deduplicated list of search results from all queries
    
    Raises:
        Exception: If any search fails
    """
    try:
        logger.info(f"Starting multiple searches for {len(queries)} queries")
        
        # Run all searches concurrently
        search_tasks = [search(query) for query in queries]
        all_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Flatten results and collect URLs for deduplication
        seen_urls: Set[str] = set()
        deduplicated_results = []
        
        for results in all_results:
            if isinstance(results, Exception):
                logger.error(f"Error in one of the searches: {str(results)}")
                continue
            
            for result in results:
                url = result.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    deduplicated_results.append(result)
        
        logger.info(f"Multiple searches completed - Total deduplicated results: {len(deduplicated_results)}")
        return deduplicated_results
    
    except Exception as e:
        logger.error(f"Error in search_multiple: {str(e)}")
        raise
