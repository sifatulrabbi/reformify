from datetime import datetime, timedelta, timezone
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.tools import Tool
from agent.base import OPENAI_MODEL, OPENAI_API_KEY

__all__ = ["CoverLetterAgent"]


def get_current_time(*args, **kwargs):
    print("provided args & kwargs:", args, kwargs)
    return datetime.now(timezone.utc).isoformat()


def add_days_to_datetime(timestamp: str, days_to_add: int):
    now = datetime.now(timezone.utc)
    future_time = now + timedelta(days=days_to_add)
    return future_time.isoformat()


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
outliner_tool = None
skill_extractor_tool = None
research_tool = None
expert_writer_tool = None
final_reviser_too = None


class CoverLetterAgent:
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
                    """You are a helpful agent. Your one and only taks is to write a '{content_type}' for the user by utilizing all the available tools and thoroughly analyzing the given job's description.

Let's progress step by step.
- First create an outline of what to do by using the 'outliner_tool' tool.
- Nextly, use the 'skill_extractor_tool' tool to figure out what makes the user the best fit for the job.
- Now, use the 'research_tool' tool to understand the best way to write a '{content_type}' based on the job description.
- Finally write the '{content_type}' using the 'expert_writer_tool' tool. Make sure you provide all the previous tool outputs to this tool.
- Use the 'final_reviser_too' tool to revise the generated content and if it tell you to redo the process then keep redoing it.

IMPORTANT: Make sure to provide the full job description to the tool.
IMPORTANT: Make sure to use the available tools to complete one or all of these above mentioned steps.

Let's begin!""",
                ),
                (
                    "human",
                    """Write me a '{content_type}' for the following job description.
<job-description>
{job_description}
</job-description>""",
                ),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._tools = [
            get_current_time_tool,
            add_days_to_datetime_tool,
        ]
        self._llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        self._agent = create_tool_calling_agent(self._llm, self._tools, self._prompt)
        self._exec = AgentExecutor(agent=self._agent, tools=self._tools)

    def execute(self, userinput: str):
        res = self._exec.invoke({"input": userinput})
        return res
