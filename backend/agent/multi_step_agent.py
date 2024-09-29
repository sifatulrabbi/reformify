import os
from typing import Union
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.agent import AgentOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

__all__ = ["MultiStepAgent"]


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found")

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


class OutlinerTool:
    # class Payload(BaseModel):
    #     content_type: str = Field(
    #         description="Type of the content to generate i.e. 'Upwork Proposal', 'Cover letter', etc"
    #     )
    #     job_description: str = Field(description="The description of the job")
    name = "outliner_tool"
    description = "Outliner tool will create an outline when generating contents. Make sure to use this tool to understand how to best generate the requested content."

    @staticmethod
    def toolfn(job_description: str):
        prompt = [
            SystemMessage(
                f"""You are an expert analyst. You will help the user by outlining the key points and requirements of a job description. The user's intent is to write a application/letter.
Think thoroughly and note down:
- the key requirements of the job
- grasp the employers intent and relay it to the user so that they can craft the prfect application/letter
- always reply in bullet points and don't include any explanation

IMPORTANT: Don't make up information only provide and use the infromation available in the job post.
Now create an outline for the given job description."""
            ),
            HumanMessage(
                f"Here is my job description:\n\n{job_description}\n\nPlease give me an outline for application/letter"
            ),
        ]
        llm = ChatOpenAI(verbose=True, model=OPENAI_MODEL)
        response = llm.invoke(prompt)
        if not isinstance(response.content, str):
            raise TypeError(
                f"Expected return type to be 'str' found '{type(response.content)}'"
            )
        return response


class SimpleOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        return AgentAction("outliner_tool", "", text)


class MultiStepAgent:
    def __init__(self):
        self._prepare_tools()
        self._prepare_prompt()
        self._prepare_agent()

    def execute(self, job_description: str):
        result = self.exec.invoke({"input": job_description})
        return result

    def _prepare_tools(self):
        self._tools: list[Tool] = [
            Tool(OutlinerTool.name, OutlinerTool.toolfn, OutlinerTool.description)
        ]

    def _prepare_prompt(self):
        system_msg = """You are a helpful agent. Your one and only taks is to write formal/informal applications and letters for the user. You will write contents such as 'Upwork Proposal', 'Cover Letter', 'Job Application', and other formal or informal applications/letters. You have access to the following tools:

{tools}
{tool_names}

- You should first understand the job's description and create an outline of what to do.
- Nextly you'll figure how the user best matches the job's requirements.
- Figure out the best way to write the user requested application/letter.
- Finally write the user requested application/letter.
- Revise and adjust the application/letter till you feel comfortable.

IMPORTANT: Make sure to use the available tools to complete one or all of these above mentioned steps.

Let's begin!

<job-description>
{input}
</job-description>

{agent_scratchpad}"""
        self._prompt = PromptTemplate.from_template(system_msg)

    def _prepare_agent(self):
        self._llm = ChatOpenAI(model=OPENAI_MODEL)
        self._agent = create_react_agent(
            self._llm, self._tools, self._prompt  # , output_parser=SimpleOutputParser
        )
        self.exec = AgentExecutor.from_agent_and_tools(self._agent, self._tools)
