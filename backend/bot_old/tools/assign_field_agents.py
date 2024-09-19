from icecream import ic
from services.bookings import BookingsService
from services.xbooker_api import XBookerAPIService
from .xagent_tool import XAgentTool


class AssingFieldAgentTool(XAgentTool):
    def __init__(self, *, org_id: str, api_service: XBookerAPIService):
        self._orgid = org_id
        self._service = BookingsService(api=api_service, org_id=self._orgid)

    @property
    def name(self) -> str:
        return "assign_field_agent_to_a_booking"

    @property
    def description(self) -> str:
        return """Useful when assigning a field agent to a booking. This tool can only assing available field agents to unhandled jobs (bookings). It need the field agent's ID and the bookings' ID to perform the task.

        field_agent_id (str, required): The ID of the field agent. This is required.
        booking_id (str, required): The ID of the booking. This is required."""

    async def tool_func(self, field_agent_id: str, booking_id: str) -> str:
        """Assigns a field agent to a booking to handle the job.

        Args:
            booking_id (str, required): The booking's ID. this is required.
            field_agent_id (str, required): This is the field agent's id. this is required.

        Returns:
            str: The success message or the error message."""
        try:
            res = await self._service.assign_field_agent(
                field_agent_id=field_agent_id, booking_id=booking_id
            )
            return res
        except Exception as e:
            ic(e)
            return f"Failed to assign the field angent to the booking.\nError: {str(e)}"
