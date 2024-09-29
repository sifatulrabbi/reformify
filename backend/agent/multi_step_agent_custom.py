from datetime import datetime, timedelta, timezone
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.tools import Tool
from agent.base import OPENAI_MODEL, OPENAI_API_KEY

__all__ = ["CustomMultiStepAgent"]


def get_current_time(*args, **kwargs):
    print("provided args & kwargs:", args, kwargs)
    return datetime.now(timezone.utc).isoformat()


def add_days_to_datetime(timestamp: str, days_to_add: int):
    now = datetime.now(timezone.utc)
    future_time = now + timedelta(days=days_to_add)
    return future_time.isoformat()


def test_tool_func(testid):
    def _return_fn(*args, **kwargs):
        print(f"Running test: {testid}.")
        print(f"toolid({testid}) args recived:", args, kwargs)
        return f"completed test: {testid}"

    return _return_fn


get_current_time_tool = Tool(
    "get_current_time_tool",
    get_current_time,
    "Use this tool to get the current time in ISO format.",
)
add_days_to_datetime_tool = Tool(
    "add_days_to_datetime_tool",
    add_days_to_datetime,
    "Add N amount of days to a timesamp then return the future timestamp. Provide a 'timestamp' and a 'days_to_add' to get the future timestamp.",
)
test_tool_one = Tool(
    "test_tool_one",
    test_tool_func(1),
    "This is test tool one and should only be ran if the user asks for 'run test suite'",
)
test_tool_two = Tool(
    "test_tool_two",
    test_tool_func(2),
    "This is test tool two and should only be ran if the user asks for 'run test suite'.",
)
test_tool_three = Tool(
    "test_tool_three",
    test_tool_func(3),
    "This is test tool three and should only be ran if the user asks for 'run test suite'.",
)
test_tool_four = Tool(
    "test_tool_four",
    test_tool_func(4),
    "This is test tool four and should only be ran if the user asks for 'run test suite'.",
)
test_tool_five = Tool(
    "test_tool_five",
    test_tool_func(5),
    "This is test tool five and should only be ran if the user asks for 'run test suite'.",
)
test_tool_six = Tool(
    "test_tool_six",
    test_tool_func(6),
    "This is test tool six and should only be ran if the user asks for 'run test suite'.",
)
test_tool_seven = Tool(
    "test_tool_seven",
    test_tool_func(7),
    "This is test tool seven and should only be ran if the user asks for 'run test suite'.",
)
test_tool_eight = Tool(
    "test_tool_eight",
    test_tool_func(8),
    "This is test tool eight and should only be ran if the user asks for 'run test suite'.",
)
test_tool_nine = Tool(
    "test_tool_nine",
    test_tool_func(9),
    "This is test tool nine and should only be ran if the user asks for 'run test suite'.",
)
test_tool_ten = Tool(
    "test_tool_ten",
    test_tool_func(10),
    "This is test tool ten and should only be ran if the user asks for 'run test suite'.",
)


class CustomMultiStepAgent:
    """Multi step agent to write cover letters or upwork proposals

    Process:
    - Identify user's strengths and key skills
    - Create an outline for the application/letter
    - Write the letter
    - Review and improve
    - Return results
    """

    def __init__(self):
        self._prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    "You are a helpful AI bot. Your name is 'ABot'. If the user asks you for 'run test suite' then you'll run all the test tools sequentially. You may also pass the test tool outputs to the next test tool.",
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._tools = [
            get_current_time_tool,
            add_days_to_datetime_tool,
            test_tool_one,
            test_tool_two,
            test_tool_three,
            test_tool_four,
            test_tool_five,
            test_tool_six,
            test_tool_seven,
            test_tool_eight,
            test_tool_nine,
            test_tool_ten,
        ]
        self._llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        self._agent = create_tool_calling_agent(self._llm, self._tools, self._prompt)
        self._exec = AgentExecutor(agent=self._agent, tools=self._tools)

    def custom_execute(self, userinput: str):
        res = self._agent.invoke({"input": userinput})
        return res

    def execute(self, userinput: str):
        res = self._exec.invoke({"input": userinput})
        return res
