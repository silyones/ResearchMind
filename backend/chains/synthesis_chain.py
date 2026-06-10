from datetime import datetime, timezone

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

from backend.models.schemas import ResearchBrief
from backend.chains.output_parser import parse_research_output, get_format_instructions
from backend.config import settings
from backend.utils.logger import get_logger
from backend.utils.text_limits import truncate_text

logger = get_logger(__name__)


SYNTHESIS_PROMPT = PromptTemplate(
    input_variables=["topic", "raw_results", "format_instructions", "generated_at"],
    template="""You are a senior research analyst preparing a client-ready research brief.

TOPIC: {topic}
CURRENT UTC TIMESTAMP: {generated_at}

WEB SEARCH RESULTS:
{raw_results}

WRITING RULES:
1. Write like a professional research report — not a list of links or one-line summaries.
2. Name specific products, models, organizations, dates, and facts found in the search results.
3. The "report" field is the main deliverable. Use markdown with these sections:
   ## Background
   ## Analysis
   ## Key Developments
   ## Implications
   ## Conclusion
   Each section must contain full paragraphs of analysis (minimum 5 paragraphs total).
4. "overview" = 2-3 sentence executive summary of the entire report.
5. "key_findings" = 3-5 detailed findings (2-4 sentences each) with concrete facts.
6. "conclusion" = 1-2 paragraph synthesis separate from the report conclusion section.
7. "sources" = every URL from the search results with title, url, and date (use "Unknown" if missing).
8. Set "generated_at" to the CURRENT UTC TIMESTAMP above in ISO-8601 format.
9. Do NOT invent facts not supported by the search results. If data is limited, state that explicitly.
10. Never write vague statements like "has released new models" without naming the models.

{format_instructions}

Return ONLY valid JSON. No markdown code fences or extra commentary.""",
)


async def synthesize(topic: str, raw_results: str) -> ResearchBrief:
    """
    Synthesize raw research results into a structured ResearchBrief using LLM.
    """
    try:
        logger.info(f"Starting synthesis for topic: '{topic}'")

        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name_llm,
            temperature=0.3,
            max_tokens=settings.max_synthesis_tokens,
        )

        synthesis_chain = LLMChain(
            llm=llm,
            prompt=SYNTHESIS_PROMPT,
            verbose=True,
        )

        format_instructions = get_format_instructions()
        bounded_results = truncate_text(raw_results, settings.max_context_chars)
        generated_at = datetime.now(timezone.utc).isoformat()

        logger.info("Running synthesis chain...")
        result = await synthesis_chain.arun(
            topic=topic,
            raw_results=bounded_results,
            format_instructions=format_instructions,
            generated_at=generated_at,
        )

        logger.info("Synthesis chain completed, parsing output...")
        research_brief = parse_research_output(result)

        logger.info(f"Synthesis completed successfully for topic: '{topic}'")
        return research_brief

    except Exception as e:
        logger.error(f"Error during synthesis for topic '{topic}': {str(e)}")
        raise
