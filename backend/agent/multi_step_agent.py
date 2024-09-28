from langchain.agents import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import convert_runnable_to_tool, BaseTool
from langchain_openai import ChatOpenAI

__all__ = ["MultiStepAgent"]

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


class MultiStepAgent:
    def __init__(self, tools: list = [], *, system_message: SystemMessage):
        self._available_tools = tools
        self._system_prompt = (
            SystemMessage("You are an inteligent and helpful agent.")
            if not system_message
            else system_message
        )

    def _prepare_tools(self):
        self._tools: list[BaseTool] = []

    def _prepare_prompt(self):
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        self._prompt = PromptTemplate.from_template(template)

    def _prepare_agent(self):
        self._llm = ChatOpenAI(verbose=True, model=OPENAI_MODEL)
        self._agent = create_react_agent(
            self._llm, tools=self._tools, prompt=self._prompt
        )

    def _outliner_agent(self):
        pass
