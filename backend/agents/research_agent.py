import asyncio
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


async def run_research(topic: str) -> ResearchBrief:
    try:
        logger.info(f"Starting research for topic: '{topic}'")
        
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name_llm,
            temperature=0.3,
        )
        
        web_search_tool = Tool(
            name="web_search",
            func=web_search,
            description="Search the web for current information on a topic. Use this to gather information about the research topic.",
        )
        
        tools = [web_search_tool]
        
        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=RESEARCH_AGENT_PROMPT,
        )
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )
        
        logger.info(f"Running agent for topic: '{topic}'")
        
        loop = asyncio.get_event_loop()
        agent_result = await loop.run_in_executor(
            None,
            lambda: agent_executor.invoke(
                {"input": f"Research the following topic and gather comprehensive information: {topic}"}
            ),
        )
        
        # Get agent final output
        raw_output = agent_result.get("output", "")
        
        # If agent hit iteration limit, extract from intermediate steps instead
        if not raw_output.strip() or "iteration limit" in raw_output or "time limit" in raw_output:
            logger.warning("Agent hit iteration limit, extracting from intermediate steps...")
            steps = agent_result.get("intermediate_steps", [])
            raw_output = "\n".join(
                str(step[1]) for step in steps if step and len(step) > 1
            )
        
        logger.info(f"Agent completed for topic: '{topic}', output length: {len(raw_output)}")
        
        logger.info("Starting synthesis phase...")
        research_brief = await synthesize(topic, raw_output)
        
        logger.info(f"Research completed successfully for topic: '{topic}'")
        return research_brief
    
    except Exception as e:
        logger.error(f"Error during research for topic '{topic}': {str(e)}")
        raise