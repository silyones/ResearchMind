import asyncio
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
        
        # Get agent final answer text
        final_answer = agent_result.get("output", "")
        
        # Always extract raw search results from intermediate steps
        # so synthesis chain has real URLs and source data
        steps = agent_result.get("intermediate_steps", [])
        search_results = "\n".join(
            str(step[1]) for step in steps if step and len(step) > 1
        )
        
        if search_results:
            raw_output = f"Agent Final Answer: {final_answer}\n\nRaw Search Results:\n{search_results}"
        else:
            raw_output = final_answer
        
        logger.info(f"Agent completed for topic: '{topic}', output length: {len(raw_output)}")
        
        logger.info("Starting synthesis phase...")
        research_brief = await synthesize(topic, raw_output)
        
        logger.info(f"Research completed successfully for topic: '{topic}'")
        return research_brief
    
    except Exception as e:
        logger.error(f"Error during research for topic '{topic}': {str(e)}")
        raise