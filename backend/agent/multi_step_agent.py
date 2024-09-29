from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool, Tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

__all__ = ["MultiStepAgent"]

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


class OutlinerTool:
    class Payload(BaseModel):
        content_type: str = Field(
            description="Type of the content to generate i.e. 'Upwork Proposal', 'Cover letter', etc"
        )
        job_description: str = Field(description="The description of the job")

    @staticmethod
    def toolfn(payload: Payload) -> str:
        prompt = [
            SystemMessage(
                f"""You are an expert analyst. You will help the user by outlining the key points and requirements of a job description. The user's intent is to write a '{payload.content_type}'.
    Think thoroughly and note down:
    - the key requirements of the job
    - grasp the employers intent and relay it to the user so that they can craft the prfect '{payload.content_type}'
    - always reply in bullet points and don't include any explanation

    IMPORTANT: Don't make up information only provide and use the infromation available in the job post."""
            ),
            HumanMessage(
                f"Here is my job description:\n\n{payload.job_description}\n\nPlease give me an outline for '{payload.content_type}'"
            ),
        ]
        llm = ChatOpenAI(verbose=True, model=OPENAI_MODEL)
        response = llm.invoke(prompt)
        return str(response.content)


class MultiStepAgent:
    def __init__(self):
        self._prepare_tools()
        self._prepare_prompt()
        self._prepare_agent()

    def execute(self, job_description: str):
        result = self.exec.invoke({"input": job_description})
        return result

    def _prepare_tools(self):
        self._tools: list[BaseTool] = [
            Tool(
                name="outliner_tool",
                func=OutlinerTool.toolfn,
                description="Outliner tool will create an outline when generating contents. Make sure to use this tool to understand how to best generate the requested content.",
                args_schema=OutlinerTool.Payload,
            )
        ]

    def _prepare_prompt(self):
        template = """You are a helpful agent. Your one and only taks is to write formal/informal applications and letters for the user. You will write contents such as 'Upwork Proposal', 'Cover Letter', 'Job Application', and other formal or informal applications/letters. You have access to the following tools:

<available-tools>
{tools}
</available-tools>

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

<thoughts>
{agent_scratchpad}
</thoughts>"""

        self._prompt = PromptTemplate.from_template(template)

    def _prepare_agent(self):
        self._llm = ChatOpenAI(verbose=True, model=OPENAI_MODEL)
        self._agent = create_react_agent(self._llm, self._tools, self._prompt)
        self.exec = AgentExecutor.from_agent_and_tools(self._agent, self._tools)
