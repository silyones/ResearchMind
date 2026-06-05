from langchain.prompts import PromptTemplate

# System prompt for the ReAct research agent
RESEARCH_AGENT_PROMPT = PromptTemplate(
    input_variables=["topic", "agent_scratchpad", "tools", "tool_names"],
    template="""You are ResearchMind, an expert research assistant.

Topic: {topic}

Available Tools: {tools}
Names: {tool_names}

Search the topic from multiple angles using web_search:
1. Overview
2. Key findings
3. Controversies
4. Expert opinions

Cite all sources with URLs. Be concise.

{agent_scratchpad}""",
)
