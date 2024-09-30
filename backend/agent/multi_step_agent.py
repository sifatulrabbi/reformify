from datetime import datetime, timedelta, timezone
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_openai import ChatOpenAI
from langchain.agents import ZeroShotAgent, create_tool_calling_agent
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


def outliner_tool(content_type: str):
    def tool(job_description: str):
        """Creates an outline based on the job description and the type of the content.
        Args:
            job_description (str): The entire job description
        """
        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    f"",
                ),
                (
                    "user",
                    f"",
                ),
            ]
        )
        result = llm.invoke(prompt.messages)
        return result.content

    return Tool(
        "outliner_tool",
        tool,
        "Creates an outline based on the job description and the type of the content.",
    )


def expert_writer_tool(content_type: str):
    def tool(outline: str, job_description: str):
        """Writes the requested content based on the jobs' description and outline.
        Args:
            outline (str): The outline to follow
            job_description (str): The entire job description
        """
        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    f"You're an expert in writing '{content_type}'. Your one an only taks is to help the user in writing the perfect '{content_type}' to land an interview. Follow this outline when you're writing a '{content_type}'.\n<outline>\n{outline}\n</outline>",
                ),
                (
                    "user",
                    f"Please write me a '{content_type}'.\nHere is the job I'm applying to.\n<job-description>\n{job_description}\n</job-description>",
                ),
            ]
        )
        result = llm.invoke(prompt.messages)
        return result.content

    return Tool(
        "expert_writer_tool",
        tool,
        "Writes the requested content based on the jobs' description and outline.",
    )


def final_reviser_tool(content_type: str):
    def tool(job_description: str, content: str):
        """Revises the generated content and suggests improvements when required.
        Args:
            content (str): The generated content to revise
        """
        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    f"You have keep eyes and your experience as a HR makes you the right one who would help the user to fine tune their '{content_type}'. Review the provided '{content_type}' and give the user you're honest criticism. If you think the provided '{content_type}' is okay for the given job description then reply 'OK' otherwise structure your criticisms in bullet points and reply to the user.",
                ),
                (
                    "user",
                    f"Please review this following '{content_type}'\n<content>\n{content}\n</content>\n\nThis is the job I'm applying to.\n<job-description>\n{job_description}\n</job-description>",
                ),
            ]
        )
        result = llm.invoke(prompt.messages)
        return result.content

    return Tool(
        "final_reviser_tool",
        tool,
        "Revises the generated content and suggests improvements when required.",
    )


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
skill_extractor_tool = None


class CoverLetterAgent:
    def __init__(
        self, user_id: str = "test-user-01", content_type: str = "Upwork Proposal"
    ):
        """Multi step agent to write cover letters or upwork proposals

        Args:
        - user_id: str - Id of the user.
        - content_type: str - The type of content the Agent should generate. i.e. Upwork Proposal, Cover Letter, etc.

        Process:
        - Identify user's strengths and key skills
        - Create an outline for the application/letter
        - Write the letter
        - Review and improve
        - Return results
        """

        self.user_id = user_id
        self.content_type = content_type
        self._prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    f"""You are a helpful agent. Your one and only taks is to write a '{self.content_type}' for the user by utilizing all the available tools and thoroughly analyzing the given job's description.

Let's progress step by step.
- Firstly, create an outline of what to do by using the 'outliner_tool' tool.
- Nextly, use the 'skill_extractor_tool' tool to figure out what makes the user the best fit for the job.
- Finally, write the '{self.content_type}' using the 'expert_writer_tool' tool. Make sure you provide all the previous tool outputs to this tool.
- After you're done writing, use the 'final_reviser_too' tool to revise the generated content and if it tell you to redo the process then keep redoing it.

IMPORTANT: Make sure to provide the full job description to the tool.
IMPORTANT: Make sure to use the available tools to complete one or all of these above mentioned steps.

Let's begin!""",
                    # When you're using a tool you should always follow this following format
                    # <format>
                    # Action: tool_name[arguments]
                    # </format>
                    #
                    # <example>
                    # Thought: I need to generate an outline for my tasks using the given job description
                    # Action: outliner_tool[The entire job description here...]
                    # </example>
                ),
                (
                    "human",
                    f"Write me a '{self.content_type}' for the following job description.\n"
                    + "<job-description>\n{job_description}\n</job-description>",
                ),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._tools = [
            get_current_time_tool,
            add_days_to_datetime_tool,
            skill_extractor_tool,
            outliner_tool(self.content_type),
            research_tool(self.content_type),
            expert_writer_tool(self.content_type),
            final_reviser_tool(self.content_type),
        ]
        self._llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        self._agent = create_tool_calling_agent(self._llm, self._tools, self._prompt)
        self._exec = AgentExecutor(agent=self._agent, tools=self._tools)

    def execute(self, userinput: str):
        res = self._exec.invoke({"input": userinput})
        return res
