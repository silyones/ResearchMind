from backend.agents.research_agent import run_research
from backend.memory.memory_manager import add_interaction, build_context_prompt
from backend.models.schemas import ResearchResponse
from backend.utils.logger import get_logger

logger = get_logger(__name__)


async def conduct_research(topic: str, session_id: str) -> ResearchResponse:
    """
    Conduct research on a given topic and save results to session memory.
    
    Args:
        topic: The research topic
        session_id: Session identifier for memory management
    
    Returns:
        ResearchResponse with success status and research brief
    """
    try:
        logger.info(f"Starting research for topic: '{topic}' (session: {session_id})")
        
        # Run the research agent
        research_brief = await run_research(topic)
        
        # Save to memory for follow-ups
        logger.info(f"Saving research interaction to memory for session {session_id}")
        add_interaction(
            session_id=session_id,
            human=topic,
            ai=research_brief.model_dump_json()
        )
        
        logger.info(f"Research completed successfully for topic: '{topic}'")
        return ResearchResponse(success=True, data=research_brief)
    
    except Exception as e:
        logger.error(f"Error conducting research for topic '{topic}': {str(e)}")
        return ResearchResponse(success=False, error=str(e))


async def followup_research(question: str, session_id: str) -> ResearchResponse:
    """
    Conduct follow-up research with awareness of prior conversation history.
    
    Args:
        question: The follow-up question or topic
        session_id: Session identifier for memory management
    
    Returns:
        ResearchResponse with success status and research brief
    """
    try:
        logger.info(f"Starting follow-up research for question: '{question}' (session: {session_id})")
        
        # Build context-aware prompt with conversation history
        context_prompt = build_context_prompt(session_id, question)
        logger.debug(f"Built context prompt with prior history for session {session_id}")
        
        # Run the research agent with context
        research_brief = await run_research(context_prompt)
        
        # Save to memory for future follow-ups
        logger.info(f"Saving follow-up interaction to memory for session {session_id}")
        add_interaction(
            session_id=session_id,
            human=question,
            ai=research_brief.model_dump_json()
        )
        
        logger.info(f"Follow-up research completed for question: '{question}'")
        return ResearchResponse(success=True, data=research_brief)
    
    except Exception as e:
        logger.error(f"Error conducting follow-up research for question '{question}': {str(e)}")
        return ResearchResponse(success=False, error=str(e))
