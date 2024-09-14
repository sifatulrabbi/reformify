from typing import Optional
from services.bookings import BookingsService
from services.xbooker_api import XBookerAPIService

from .xagent_tool import XAgentTool


class SendBookingInvitationTool(XAgentTool):
    """Sends booking invitation to email addresses on behalf of an organization."""

    def __init__(self, *, user_id: str, org_id: str, api_service: XBookerAPIService):
        self._user_id = user_id
        self._org_id = org_id
        self._service = BookingsService(api=api_service, org_id=self._org_id)

    @property
    def name(self) -> str:
        return "send_booking_email_to_client_email"

    @property
    def description(self) -> str:
        return """Useful when sending booking invitations to a client's email address with or without discounts. The tool takes in a client_email which is required to send the booking invitation. If the user didn't provide a client_email then ask for the email. The tool can also take in a discount which needs to be an integer, for example 10% will be 10."""

    async def tool_func(self, client_email: str, discount: Optional[int] = 0) -> str:
        """Sends a booking email to the specified client's email address.

        Args:
            client_email (str): The client email where the booking invitation will be sent.
            discount (int, optional): The amount of discount for the booking invitation. Defaults to 0.

        Returns:
            str: Success message or an error message based on the results.
        """
        if not self._org_id:
            return "No organization's id found in the current session."
        if not self._user_id:
            return "User's id not found in the current session."
        if not client_email:
            return "client_email wasn't specified in the request payload."

        err = await self._service.send_booking_invitation(
            client_email=client_email,
            sender_id=self._user_id,
            sender_name="",  # TODO: implement user information gather logic, so that the bot can know to which organization the user belongs to.
            discount=discount,
        )
        return err if err else "The booking invitation was sent successfully"
