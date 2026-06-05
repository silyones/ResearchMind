import json
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_groq import ChatGroq
from backend.models.schemas import ResearchBrief
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize base parser for ResearchBrief
base_parser = PydanticOutputParser(pydantic_object=ResearchBrief)

# Create LLM for fixing malformed output
fixing_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model_name=settings.model_name_llm,
    temperature=0,
)

# Wrap with OutputFixingParser for auto-correction
output_parser = OutputFixingParser.from_llm(
    llm=fixing_llm,
    parser=base_parser,
)


def parse_research_output(text: str) -> ResearchBrief:
    """
    Parse research output text into a ResearchBrief using Pydantic validation.
    
    Automatically fixes malformed JSON using the OutputFixingParser.
    
    Args:
        text: Raw output text from the LLM
    
    Returns:
        Parsed ResearchBrief object
    
    Raises:
        Exception: If parsing fails after fixing attempts
    """
    try:
        logger.info("Parsing research output into ResearchBrief")
        research_brief = output_parser.parse(text)
        logger.info("Research output parsed successfully")
        return research_brief
    except Exception as e:
        logger.error(f"Failed to parse research output: {str(e)}")
        raise


def get_format_instructions() -> str:
    """Get format instructions for the LLM output."""
    return base_parser.get_format_instructions()
