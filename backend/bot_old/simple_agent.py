import openai
import json
import os
from typing import Any, List, Dict, Callable, Union

from .configs import GPTModels
from .simple_agent_tools import SimpleXAgentTools


openai.api_key = os.getenv("OPENAI_API_KEY", "")


class SimpleXAgentPrompt:
    """
    Simple X-Agent's prompt. This prompt is able to memorize the message history of an user.

    Note: For now the agent uses local disk to store chats.
    """

    _system_prompt = {
        "role": "system",
        "content": """You are a helpful agent who supports the users with managing their business. You will send booking invitations or booking links to the user's client emails with or without discounts. You will also help them with querying booking requests submitted to their organization, and also with querying their todo list using the tools provided to you. If you think the user did not provided enough information to complete a task or query then you will ask them to provide those information.
        
        When you send booking information or todo list information to the user make sure to format it with Markdown syntax to make the data more human readable.""",
        # "You are a agent who helps users with sending booking invitations to their clients. If an user requests to send a booking invitation without specifying their client email address then you will ask them to specify their client email address.",
    }

    def __init__(self, user_id: str) -> None:
        # before saving the prompt message make sure that a .cache folder exists.
        if not os.path.exists(".cache"):
            os.makedirs(".cache", exist_ok=True)
        self._user_id = user_id
        self._cache_filename = f".cache/{self._user_id}.json"
        self._messages = self._load_stored_messages()
        self._store_messages()

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def messages(self) -> List[Dict[str, str]]:
        return self._messages

    def add_message(self, content: str, role: str, name: str | None = None):
        """
        Adds a new message to the `messages` list

        Args:
        - content `str`: The message body.
        - role `"user"` | `"assistant"` | `"function"`: The role of the message sender.
        """
        if role not in ["assistant", "user", "function"]:
            raise ValueError("role should be either 'user', 'function' or 'assistant'")
        new_msg = {"role": role, "content": content}
        if name:
            new_msg["name"] = name
        self._load_stored_messages()
        self._messages.append(new_msg)
        self._store_messages()

    def reset_history(self) -> None:
        """
        Resets the chat history of the selected user.
        """
        self._messages = []
        self._store_messages()
        self._messages = [self._system_prompt]

    def _store_messages(self):
        """
        Stores all the current messages in to a JSON file.
        """
        messages_to_be_stored = [
            msg for msg in self._messages if msg["role"] != "system"
        ]
        str_messages = json.dumps(messages_to_be_stored, indent=2)
        with open(self._cache_filename, "w") as f:
            f.write(str_messages)

    def _load_stored_messages(self) -> List[Dict]:
        """
        Get all the stored messages.
        """
        if not os.path.exists(self._cache_filename):
            return [self._system_prompt]
        with open(self._cache_filename, "r") as f:
            content = f.read()
        if not content:
            return [self._system_prompt]
        messages: List[Dict] = json.loads(content)
        if len(messages) < 1:
            return [self._system_prompt]
        messages = [
            self._system_prompt,
            *[msg for msg in messages if msg["role"] != "system"],
        ]
        return messages


class SimpleXAgent:
    """
    Simple X-Agent built using the openai only.
    """

    def __init__(self, tools: SimpleXAgentTools) -> None:
        self._tools = tools

    def run(
        self,
        msg: str,
        user_session: Dict,
    ) -> str:
        """Run the agent and generate response.

        Args:
            msg (str): User's message.
            user_id (str): User's id.
            org_id (str): ID of the organization the user belongs to.
            user_session (dict): The current session info.

        Returns:
            str: The response message.
        """
        # ic(f"user_message: {msg}")
        user_id = user_session.get("id")
        prompt = SimpleXAgentPrompt(user_id)
        prompt.add_message(msg, "user")
        # get the first chat completion and look for function_call
        response: Dict[str, List[Dict]] = openai.ChatCompletion.create(
            model=GPTModels.gpt_35,
            messages=prompt.messages,
            functions=self._tools.available_tools,
            function_call="auto",
        )
        response_msg: Dict[str, Dict] = response.get("choices")[0].get("message")
        function_call: Union[Dict[str, str], None] = response_msg.get("function_call")
        # if the gpt is not trying to call a function then return without any 2nd invocation.
        if not function_call:
            # return ic(self._parse_openai_response(response_msg))
            return self._parse_openai_response(response_msg)
        # if there is a function_call then find and call the function with the given args.
        function_name = function_call.get("name")
        function_to_call: Callable = self._tools.tools_map.get(function_name)
        function_args = json.loads(function_call.get("arguments"))
        function_response: Dict[str, Any] = function_to_call(
            function_args, user_session
        )
        # create another chat completion with gpt for the final result.
        prompt.add_message(function_response, "function", function_name)
        second_response = openai.ChatCompletion.create(
            model=GPTModels.gpt_35,
            messages=prompt.messages,
        )
        # reset the chat history right after sending the bolling invitation.
        prompt.reset_history()
        # return ic(self._parse_openai_response(second_response))
        return self._parse_openai_response(second_response)

    def _parse_openai_response(self, resp: Dict) -> str:
        """
        Parses the OpenAI API's response and only returns a string.

        Args:
        - resp `dict`: The openai api's response dict.

        Returns:
        - `str`
        """
        choices: Union[List[Dict], None] = resp.get("choices")
        content: Union[str, None] = resp.get("content")
        if not choices and content:
            return content
        elif choices:
            msg: str = choices[0].get("message").get("content")
            return msg
        else:
            return "The bot wasn't able to reply at the moment. Please try again."
