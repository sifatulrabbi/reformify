from services.bookings import BookingsService
from services.xbooker_api import XBookerAPIService
from .xagent_tool import XAgentTool


class RemoveBookingTool(XAgentTool):
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return "delete_a_booking_request_tool"

    @property
    def description(self) -> str:
        return """This tool is useful when removing a booking request from a organization.
        Required params:
        org_id (str): User's organization id. this field is required to find the right organization.
        id (str): the booking's id. this fied is required to find and remove the booking request."""

    async def tool_func(
        self, org_id: str, id: str, api_service: XBookerAPIService
    ) -> str:
        """Removes a booking request from the organizatoin.

        Args:
            org_id (str): The id of the user's organization.
            id (str): The id of the booking. Required

        Returns:
            str: The success message or the error message.
        """
        try:
            bookings_service = BookingsService(api=api_service, org_id=org_id)
            res = await bookings_service.remove_booking(id)
            return res
        except Exception as e:
            print(e)
            return str(e)
