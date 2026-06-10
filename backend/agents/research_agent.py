from backend.chains.synthesis_chain import synthesize
from backend.models.schemas import ResearchBrief
from backend.services.tavily_service import search as tavily_search
from backend.utils.logger import get_logger
from backend.utils.search_format import format_search_results

logger = get_logger(__name__)


async def run_research(topic: str) -> ResearchBrief:
    """Search the web once, then synthesize a structured research report."""
    try:
        logger.info(f"Starting research for topic: '{topic}'")

        search_query = f"{topic} latest developments detailed analysis"
        results = await tavily_search(search_query)
        raw_output = format_search_results(results)

        logger.info(
            f"Search completed for topic: '{topic}', "
            f"{len(results)} results, {len(raw_output)} chars"
        )

        research_brief = await synthesize(topic, raw_output)

        logger.info(f"Research completed successfully for topic: '{topic}'")
        return research_brief

    except Exception as e:
        logger.error(f"Error during research for topic '{topic}': {str(e)}")
        raise
