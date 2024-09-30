import logging
from datetime import datetime, timedelta, timezone
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_tool_calling_agent
from langchain.tools import Tool
from agent.base import OPENAI_MODEL, OPENAI_API_KEY

__all__ = ["CoverLetterAgent"]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_current_time(*args, **kwargs):
    print("provided args & kwargs:", args, kwargs)
    return datetime.now(timezone.utc).isoformat()


get_current_time_tool = Tool(
    "get_current_time_tool",
    get_current_time,
    "Use this tool to get the current time in ISO format.",
)


def add_days_to_datetime(timestamp: str, days_to_add: int):
    now = datetime.now(timezone.utc)
    future_time = now + timedelta(days=days_to_add)
    return future_time.isoformat()


add_days_to_datetime_tool = Tool(
    "add_days_to_datetime_tool",
    add_days_to_datetime,
    "Add N amount of days to a timesamp then return the future timestamp. Provide a 'timestamp' and a 'days_to_add' to get the future timestamp.",
)


def outliner_tool(content_type: str, job_description: str):
    def tool(*_):
        """Creates an outline based on the job description and the type of the content."""
        print("-" * 80)
        logging.info(f"using 'outliner_tool'")
        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = [
            SystemMessage(
                f"Your one and only task is to outline what needs to be done in order to write the perfect '{content_type}' for the provided job description. IMPORTANT: you should only write the outline in bullet points and do not provide any explanation or examples."
            ),
            HumanMessage(
                f"Please write me a '{content_type}' for this following job description.\n<job-description>\n{job_description}\n</job-description>"
            ),
        ]
        result = llm.invoke(prompt)
        print(result.content)
        logging.info("done using 'outliner_tool'. returning results...")
        print("-" * 80)
        return result.content

    return Tool(
        "outliner_tool",
        tool,
        "Creates an outline based on the job description and the type of the content.",
    )


def expert_writer_tool(content_type: str, job_description: str):
    def tool(outline: str):
        """Writes the requested content based on the jobs' description and outline.
        Args:
            outline (str): Provide the outline to follow when writing
        """
        print("-" * 80)
        logging.info(f"using 'expert_writer_tool'")
        print("outline:", outline)
        print("-" * 10)
        if not job_description or not outline:
            raise ValueError("arg 'job_description' or 'outline' is not provided")

        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = [
            SystemMessage(
                f"You're an expert in writing '{content_type}'. Your one an only taks is to help the user in writing the perfect '{content_type}' to land an interview. Follow this outline when you're writing a '{content_type}'.\n<outline>\n{outline}\n</outline>\n\nIMPORTANT: You should only write what is requested and do not provide any explanation or examples.",
            ),
            HumanMessage(
                f"Please write me a '{content_type}'.\nHere is the job I'm applying to.\n<job-description>\n{job_description}\n</job-description>",
            ),
        ]
        result = llm.invoke(prompt)
        print(result.content)
        logging.info("done using 'expert_writer_tool'. returning results...")
        print("-" * 80)
        return result.content

    return Tool(
        "expert_writer_tool",
        tool,
        "Writes the requested content based on the jobs' description and outline.",
    )


def final_reviser_tool(content_type: str, job_description: str):
    def tool(content: str):
        """Revises the generated content and suggests improvements when required.
        Args:
            content (str): Provide the content to revise
        """
        logging.info(f"using 'final_reviser_tool'")
        print("-" * 80)
        print("content:", content)
        print("-" * 10)
        if not job_description or not content:
            raise ValueError("arg 'job_description' or 'content' is not provided")

        llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        prompt = [
            SystemMessage(
                f"You have keen eyes and your experience as a HR makes you the right one who would help the user to fine tune their '{content_type}'. Review the provided '{content_type}' and give the user you're honest criticism. If you think the provided '{content_type}' is okay for the given job description then reply 'The content is OK' otherwise structure your criticisms in bullet points and reply to the user. Do not provide any examples or long explanation only bullet points.",
            ),
            HumanMessage(
                f"Please review this following '{content_type}'\n<content>\n{content}\n</content>\n\nThis is the job I'm applying to.\n<job-description>\n{job_description}\n</job-description>",
            ),
        ]
        result = llm.invoke(prompt)
        print(result.content)
        logging.info("done using 'final_reviser_tool'. returning results...")
        print("-" * 80)
        return result.content

    return Tool(
        "final_reviser_tool",
        tool,
        "Revises the generated content and suggests improvements when required.",
    )


class CoverLetterAgent:
    def __init__(
        self,
        job_description: str,
        user_id: str = "test-user-01",
        content_type: str = "Upwork Proposal",
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

        self.job_description = job_description
        self.user_id = user_id
        self.content_type = content_type
        self._prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    """You are a helpful agent. Your one and only taks is to write a '{content_type}' for the user by utilizing all the available tools and thoroughly analyzing the given job's description.

You have these tools available to you, make use of these tools when necessary:
- 'outliner_tool' (Creates an outline based on the job description and the type of the content. Does not take in any arguments.)
- 'expert_writer_tool' (Writes the requested content based on the jobs' description and outline. Takes in the generated outline as the argument.)
- 'final_reviser_tool' (Revises the generated content and suggests improvements when required. Takes in the generated content as the argument.)

Let's progress step by step.
- Firstly, create an outline of what to do by using the 'outliner_tool' tool.
- Now write the '{content_type}' using the 'expert_writer_tool' tool. You should provide the outputs from 'outliner_tool' to the 'expert_writer_tool'.
- After you're done writing, use the 'final_reviser_too' tool to revise the generated content and if it tells you to redo the process then keep redoing it. You should provide the outputs from 'expert_writer_tool' to the 'final_reviser_tool'.

IMPORTANT: Make sure to provide the full job description to the tool.
IMPORTANT: Make sure to use the available tools to complete one or all of these above mentioned steps.

Let's begin!""",
                ),
                (
                    "human",
                    "Write me a '{content_type}' for the following job description.\n<job-description>\n{job_description}\n</job-description>",
                ),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._tools = [
            get_current_time_tool,
            add_days_to_datetime_tool,
            outliner_tool(self.content_type, self.job_description),
            expert_writer_tool(self.content_type, self.job_description),
            final_reviser_tool(self.content_type, self.job_description),
        ]
        self._llm = ChatOpenAI(model=OPENAI_MODEL, verbose=True, api_key=OPENAI_API_KEY)
        self._agent = create_tool_calling_agent(self._llm, self._tools, self._prompt)
        self._exec = AgentExecutor(agent=self._agent, tools=self._tools)

    def execute(self):
        res = self._exec.invoke(
            {"job_description": self.job_description, "content_type": self.content_type}
        )
        return res
