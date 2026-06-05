import asyncio
import json
from typing import List, Dict, Any
from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain.tools import Tool
from backend.chains.prompts import RESEARCH_AGENT_PROMPT
from backend.chains.synthesis_chain import synthesize
from backend.models.schemas import ResearchBrief
from backend.tools.tavily_tool import web_search
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def _format_search_results(results: List[Dict[str, Any]]) -> str:
    """
    Format search results into a readable string for the agent.
    
    Args:
        results: List of search result dictionaries
    
    Returns:
        Formatted string representation of results
    """
    if not results:
        return "No results found."
    
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(
            f"{i}. Title: {result.get('title', 'N/A')}\n"
            f"   URL: {result.get('url', 'N/A')}\n"
            f"   Content: {result.get('content', 'N/A')[:300]}...\n"
            f"   Date: {result.get('published_date', 'N/A')}"
        )
    
    return "\n".join(formatted)


async def run_research(topic: str) -> ResearchBrief:
    """
    Run the ReAct research agent to gather information on a topic and synthesize into ResearchBrief.
    
    Args:
        topic: The research topic to investigate
    
    Returns:
        Comprehensive ResearchBrief with findings, sources, and analysis
    
    Raises:
        Exception: If research or synthesis fails
    """
    try:
        logger.info(f"Starting research for topic: '{topic}'")
        
        # Initialize Groq LLM for the agent
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name_llm,
            temperature=0.3,
        )
        
        # Create web_search tool for the agent
        web_search_tool = Tool(
            name="web_search",
            func=web_search,
            description="Search the web for current information on a topic. Use this to gather information about the research topic.",
        )
        
        tools = [web_search_tool]
        
        # Create the ReAct agent
        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=RESEARCH_AGENT_PROMPT,
        )
        
        # Create the AgentExecutor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=settings.max_agent_iterations,
            handle_parsing_errors=True,
        )
        
        logger.info(f"Running agent for topic: '{topic}'")
        
        # Run the agent asynchronously
        loop = asyncio.get_event_loop()
        agent_result = await loop.run_in_executor(
            None,
            lambda: agent_executor.invoke(
                {"topic": topic, "agent_scratchpad": ""}
            ),
        )
        
        # Extract raw output from agent
        raw_output = agent_result.get("output", "")
        logger.info(f"Agent completed research gathering for topic: '{topic}'")
        logger.debug(f"Agent raw output length: {len(raw_output)} characters")
        
        # Synthesize the gathered information into ResearchBrief
        logger.info("Starting synthesis phase...")
        research_brief = await synthesize(topic, raw_output)
        
        logger.info(f"Research completed successfully for topic: '{topic}'")
        return research_brief
    
    except Exception as e:
        logger.error(f"Error during research for topic '{topic}': {str(e)}")
        raise
