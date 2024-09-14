"""
All the tools for the Agent to perform different tasks based on the user's request.
"""

from typing import List
from langchain.tools import StructuredTool, BaseTool
from langchain.tools.render import format_tool_to_openai_function
from services.xbooker_api import XBookerAPIService
from .xagent_tool import XAgentTool
from .send_booking_invitations import SendBookingInvitationTool
from .query_bookings import QueryBookings
from .current_date_info import CurrentDateInfo
from .get_organization_members import GetOrganizationMembersTool


class XAgentTools:
    """Agent tools orchestrator."""

    def __init__(self, *, user_id: str, org_id: str, api_service: XBookerAPIService):
        """Initialize the Agent Tools.

        Args:
            user_id (str): The user's ID.
            org_id (str): The user's organization ID.
        """
        if not user_id or not org_id:
            raise ValueError(
                "`user_id` and `org_id` is required to instantiate the tools"
            )
        self._user_id = user_id
        self._org_id = org_id
        self._api_service = api_service
        self._available_tools: List[XAgentTool] = [
            SendBookingInvitationTool(
                user_id=self._user_id,
                org_id=self._org_id,
                api_service=self._api_service),
            QueryBookings(
                user_id=self._user_id,
                org_id=self._org_id,
                api_service=self._api_service),
            GetOrganizationMembersTool(
                org_id=self._org_id,
                api_service=self._api_service),
            CurrentDateInfo(),
        ]

    @property
    def openai_functions(self):
        functions = [format_tool_to_openai_function(
            t) for t in self.tools_list]
        return functions

    @property
    def tools_list(self) -> List[BaseTool]:
        """Get the available tools list.

        Returns:
            List[Tool]: List of `langchain.tools.Tool`
        """
        tools: List[BaseTool] = []
        for tool in self._available_tools:
            tools.append(
                StructuredTool.from_function(
                    name=tool.name,
                    description=tool.description,
                    coroutine=tool.tool_func,
                )
            )
        return tools
