from langchain.prompts import PromptTemplate

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
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT RULES:
- Do ONE search only. After getting the Observation, immediately write Final Answer.
- NEVER do a second search. One search is enough.
- Final Answer must be a detailed summary of everything in the Observation.
- Do NOT repeat the same Action Input ever.

Begin!

Question: {input}
Thought:{agent_scratchpad}""",
)