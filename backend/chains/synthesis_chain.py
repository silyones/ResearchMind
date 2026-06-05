from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from backend.models.schemas import ResearchBrief
from backend.chains.output_parser import parse_research_output, get_format_instructions
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


# Define the synthesis prompt
SYNTHESIS_PROMPT = PromptTemplate(
    input_variables=["topic", "raw_results"],
    template="""You are an expert research synthesizer. Your task is to organize and synthesize raw research data into a comprehensive research brief.

Topic: {topic}

Raw Research Results:
{raw_results}

Format Instructions:
{format_instructions}

Based on the raw results above, create a comprehensive research brief with:
1. An overview of the topic
2. Key findings (with source URLs)
3. Controversies or debates
4. Expert opinions
5. A conclusion
6. All sources used

Return ONLY valid JSON matching the format instructions above. Do not include any additional text.""",
)


async def synthesize(topic: str, raw_results: str) -> ResearchBrief:
    """
    Synthesize raw research results into a structured ResearchBrief using LLM.
    
    Args:
        topic: The research topic
        raw_results: Raw search results as formatted text
    
    Returns:
        Synthesized ResearchBrief object
    
    Raises:
        Exception: If synthesis or parsing fails
    """
    try:
        logger.info(f"Starting synthesis for topic: '{topic}'")
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name_llm,
            temperature=0.3,
            max_tokens=2048,
        )
        
        # Create the LLMChain
        synthesis_chain = LLMChain(
            llm=llm,
            prompt=SYNTHESIS_PROMPT,
            verbose=True,
        )
        
        # Format instructions for the prompt
        format_instructions = get_format_instructions()
        
        # Run the chain
        logger.info("Running synthesis chain...")
        result = await synthesis_chain.arun(
            topic=topic,
            raw_results=raw_results,
            format_instructions=format_instructions,
        )
        
        logger.info("Synthesis chain completed, parsing output...")
        
        # Parse the result using the output parser
        research_brief = parse_research_output(result)
        
        logger.info(f"Synthesis completed successfully for topic: '{topic}'")
        return research_brief
    
    except Exception as e:
        logger.error(f"Error during synthesis for topic '{topic}': {str(e)}")
        raise
