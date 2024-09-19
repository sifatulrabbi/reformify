from typing import Dict, List, Union
from services.bookings import BookingsService
from services.xbooker_api import XBookerAPIService
from icecream import ic
from .xagent_tool import XAgentTool


class GetOrganizationMembersTool(XAgentTool):
    def __init__(self, *, org_id: str, api_service: XBookerAPIService):
        self._org_id = org_id
        self._service = BookingsService(api=api_service, org_id=self._org_id)

    @property
    def name(self) -> str:
        return "get_organization_members_by_deparment"

    @property
    def description(self) -> str:
        return """Useful when requires an organization's department's member information. For example if you want to get the field agents of a organization then use this tool to get the members from the organization's fieldAgent department. If there are no members in the organization then this tool will simply return an empty list.

        department (str, required): Id of the department. Must be provided. Available departments: 'fieldAgent', 'booking', 'admin', 'sales', 'finance'"""

    async def tool_func(
        self, department: str, available_only: bool = True
    ) -> Union[List[Dict[str, str]], str]:
        """Get all the members from a department within the organization.

        Args:
            department (str, required): The id of the department. Must be provided. Available departments: 'fieldAgent', 'booking', 'admin', 'sales', 'finance'
            available_only (bool): When set to True the tool will only return members who are avialbe to take on a new job.

        Returns:
            List[Dict[str, str]], str: The error message is there are errors or the list of department members."""
        try:
            print("getting organization members", department, available_only)

            if available_only:
                res = await self._service.get_available_field_agents(
                    org_id=self._org_id
                )
            else:
                # TODO: create a new method that will get all the members regarless of their availability.
                res = await self._service.get_available_field_agents(
                    org_id=self._org_id
                )
            return res
        except Exception as e:
            ic(e)
            return f"Unable to get the members.\nError: {str(e)}"
