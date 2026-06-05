from fastapi import APIRouter, Query
from typing import List, Dict
from backend.models.schemas import ResearchRequest, ResearchResponse
from backend.services.research import conduct_research, followup_research
from backend.memory.memory_manager import get_history
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Create router
router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify backend is running.
    
    Returns:
        Status and model information
    """
    logger.debug("Health check request received")
    return {
        "status": "ok",
        "model": settings.model_name,
    }


@router.post("/research", response_model=ResearchResponse)
async def research_endpoint(
    request: ResearchRequest,
    session_id: str = Query("default", description="Session identifier for memory management")
) -> ResearchResponse:
    """
    Conduct research on a given topic.
    
    Args:
        request: ResearchRequest with topic field
        session_id: Unique session identifier (default: "default")
    
    Returns:
        ResearchResponse with research brief or error
    """
    logger.info(f"Research request received for topic: '{request.topic}' (session: {session_id})")
    
    response = await conduct_research(
        topic=request.topic,
        session_id=session_id
    )
    
    return response


@router.post("/followup", response_model=ResearchResponse)
async def followup_endpoint(
    request: Dict[str, str],
    session_id: str = Query("default", description="Session identifier for memory management")
) -> ResearchResponse:
    """
    Conduct follow-up research with conversation context.
    
    Args:
        request: Dict with "question" field
        session_id: Unique session identifier (default: "default")
    
    Returns:
        ResearchResponse with research brief or error
    """
    question = request.get("question", "")
    
    if not question:
        logger.warning("Follow-up request with empty question")
        return ResearchResponse(success=False, error="Question field is required")
    
    logger.info(f"Follow-up request received: '{question}' (session: {session_id})")
    
    response = await followup_research(
        question=question,
        session_id=session_id
    )
    
    return response


@router.get("/history/{session_id}")
async def history_endpoint(session_id: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Dict containing list of conversation exchanges
    """
    try:
        logger.info(f"History request for session: {session_id}")
        history = get_history(session_id)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error retrieving history for session {session_id}: {str(e)}")
        return {"history": []}
