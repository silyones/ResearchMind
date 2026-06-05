from langchain.prompts import PromptTemplate

# Standard ReAct prompt format from LangChain
RESEARCH_AGENT_PROMPT = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT RULES:
- NEVER repeat the same Action Input twice. If you already searched for something, do NOT search for it again.
- After 2-3 searches, stop and give your Final Answer using what you have gathered.
- If the first search gives enough information, go straight to Final Answer.
- Maximum 3 searches total, then you MUST write Final Answer.
- Final Answer should be a detailed summary of everything you found.

Begin!

Question: {input}
Thought:{agent_scratchpad}""",
)