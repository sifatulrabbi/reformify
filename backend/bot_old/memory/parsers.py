from typing import Union
from langchain.schema.messages import HumanMessage, AIMessage
from icecream import ic


def string_to_chat_history_list(msg: Union[str, None] = None):
    """Parses the string chat history in to Agent compatible `List[BaseChat]`

    Args:
        msg (str): The message history string.

    Returns:
        List[BaseChat]: The list of BaseChat objects.
    """
    messages_list = []

    if not msg:
        return messages_list
    try:
        messages = msg.split("\n")
        for message in messages:
            if message.startswith("Human: "):
                messages_list.append(HumanMessage(content=message.split("Human: ")[1]))
            if message.startswith("AI: "):
                messages_list.append(AIMessage(content=message.split("AI: ")[1]))
    except Exception as e:
        ic(e)
    finally:
        return messages_list
