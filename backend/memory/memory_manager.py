from langchain.memory import ConversationBufferMemory
from typing import Dict, List, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Global session memory store
_session_memories: Dict[str, ConversationBufferMemory] = {}


def get_memory(session_id: str) -> ConversationBufferMemory:
    """
    Get or create a ConversationBufferMemory instance for a given session.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        ConversationBufferMemory instance for the session
    """
    try:
        if session_id not in _session_memories:
            logger.info(f"Creating new memory for session: {session_id}")
            _session_memories[session_id] = ConversationBufferMemory(
                human_prefix="human_input",
                ai_prefix="ai_output",
                return_messages=False,
            )
        else:
            logger.debug(f"Returning existing memory for session: {session_id}")
        
        return _session_memories[session_id]
    
    except Exception as e:
        logger.error(f"Error getting memory for session {session_id}: {str(e)}")
        raise


def add_interaction(session_id: str, human: str, ai: str) -> None:
    """
    Add a human/ai exchange to the session's conversation memory.
    
    Args:
        session_id: Unique session identifier
        human: Human input/question
        ai: AI response
    
    Raises:
        Exception: If adding interaction fails
    """
    try:
        memory = get_memory(session_id)
        logger.debug(f"Adding interaction to session {session_id}")
        memory.save_context(
            {"human_input": human},
            {"ai_output": ai}
        )
        logger.info(f"Interaction added to session {session_id}")
    
    except Exception as e:
        logger.error(f"Error adding interaction to session {session_id}: {str(e)}")
        raise


def get_history(session_id: str) -> List[Dict[str, str]]:
    """
    Get conversation history for a session as a list of dicts.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        List of dicts with keys "role" ("user"/"assistant") and "content"
    
    Raises:
        Exception: If retrieving history fails
    """
    try:
        memory = get_memory(session_id)
        buffer = memory.buffer
        
        if not buffer:
            logger.debug(f"No history found for session {session_id}")
            return []
        
        # Parse the buffer string into structured history
        history = []
        lines = buffer.strip().split("\n")
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith("human_input:"):
                content = line.replace("human_input:", "").strip()
                history.append({"role": "user", "content": content})
            elif line.startswith("ai_output:"):
                content = line.replace("ai_output:", "").strip()
                history.append({"role": "assistant", "content": content})
            
            i += 1
        
        logger.debug(f"Retrieved history for session {session_id}: {len(history)} exchanges")
        return history
    
    except Exception as e:
        logger.error(f"Error getting history for session {session_id}: {str(e)}")
        raise


def clear_memory(session_id: str) -> None:
    """
    Clear all conversation memory for a given session.
    
    Args:
        session_id: Unique session identifier
    """
    try:
        if session_id in _session_memories:
            del _session_memories[session_id]
            logger.info(f"Memory cleared for session {session_id}")
        else:
            logger.debug(f"No memory found to clear for session {session_id}")
    
    except Exception as e:
        logger.error(f"Error clearing memory for session {session_id}: {str(e)}")
        raise


def build_context_prompt(session_id: str, new_topic: str) -> str:
    """
    Build a context prompt combining prior conversation history with a new topic.
    
    This is useful for follow-up questions where the agent needs awareness of
    previous discussions.
    
    Args:
        session_id: Unique session identifier
        new_topic: The new topic or follow-up question
    
    Returns:
        Formatted string with conversation history + new topic
    
    Raises:
        Exception: If building context fails
    """
    try:
        history = get_history(session_id)
        
        context_parts = []
        
        # Add conversation history if it exists
        if history:
            context_parts.append("=== Previous Conversation ===")
            for exchange in history:
                if exchange["role"] == "user":
                    context_parts.append(f"User: {exchange['content']}")
                elif exchange["role"] == "assistant":
                    context_parts.append(f"Assistant: {exchange['content']}")
        
        # Add the new topic/question
        context_parts.append("\n=== Current Request ===")
        context_parts.append(f"Topic/Question: {new_topic}")
        
        context_prompt = "\n".join(context_parts)
        
        logger.debug(f"Built context prompt for session {session_id}")
        return context_prompt
    
    except Exception as e:
        logger.error(f"Error building context prompt for session {session_id}: {str(e)}")
        raise
