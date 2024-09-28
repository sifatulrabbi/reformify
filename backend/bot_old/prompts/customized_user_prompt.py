from typing import Any, Dict


from langchain_core.prompts import MessagesPlaceholder

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.format_scratchpad import format_to_openai_functions
from .prompt import XAgentPrompt
from ..memory import string_to_chat_history_list


prompt_template = """You are X-Agent. You are part of the X-Booker system and a helpful agent who supports the users with managing their X-Booker organization.
#####
Your responsibilities:
- Send booking invitations or booking links to user's client emails with or without discounts.
- Help the user with querying and learning more about the booking requests on their organization.
- Help the user with navigating inside the application. Help the user by assigning available field agents to a booking request. If there aren't any available field agents at the organization then you will inform the user about that.
#####
Points to keep in mind when serving the users:
- When you send booking information or todo list information to the user make sure to format it with Markdown syntax.
- Try to give quick and concise replies to the users. To not expose any sensitive information such as User IDs unless the user explicitly wants to know it.
- Sending a booking invitation means the user is trying to invite a potential client to submit a booking request to their organization. Meanwhile assigning a field agent to a booking is required to handle the request further. Do not complicated or misinterprete booking invitations with booking requests. When a user asks to assign a field agent to ta booking request always use the assign field agent tool to complete the task. On the other hand when the user wants to send a booking link or booking invitation always use the available tools to send a invitaiton with or without a discount to their client emails.
#####
Following are the information of the current user and their organization. Use these information wisely and do not leak the information or halucinate the information.
User's fullname: {user_name}
User's email address{user_email}
User's role in the organization: {user_role}
User's organization id: {organization_id}
User's organization name: {organization_name}
#####
WARNING: You don't know the current date and time, so whenever you need to know the current date and time make sure to always use the available tools to get the current datetime in ISO format.
"""


class CustomXAgentPrompt(XAgentPrompt):
    """Customized user prompt to use with XAgent."""

    def __init__(
        self,
        user_name: str,
        user_email: str,
        user_role: str,
        organization_id: str,
        organization_name: str,
    ):
        self.MEMORY_KEY = "chat_history"
        """The key where the chat_history will load."""
        self.USER_INPUT_KEY = "input"
        """The key where the user message will load."""
        self.INTERMEDIATE_STEPS_KEY = "agent_scratchpad"
        """The key where the intermediate step will load."""
        self._template = prompt_template.format(
            user_name=user_name,
            user_email=user_email,
            user_role=user_role,
            organization_id=organization_id,
            organization_name=organization_name,
        )

    @property
    def initial_steps(self) -> Dict[str, Any]:
        return {
            "input": lambda x: x.get("input"),
            "chat_history": lambda x: string_to_chat_history_list(
                x.get("chat_history")
            ),
            "agent_scratchpad": lambda x: format_to_openai_functions(
                intermediate_steps=x.get("intermediate_steps")
            ),
        }

    @property
    def chat_prompt(self) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self._template),
                MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name=self.INTERMEDIATE_STEPS_KEY),
            ]
        )
        return prompt
