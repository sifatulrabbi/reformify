from typing import List, Union, Optional, Dict, Any
from services.xbooker_api import XBookerAPIService
from services.bookings import BookingsService

from .xagent_tool import XAgentTool


class QueryBookings(XAgentTool):
    """Filters and queries booking information from a user's organization."""

    def __init__(self, *, user_id: str, org_id: str, api_service: XBookerAPIService):
        self._user_id = user_id
        self._org_id = org_id
        self._service = BookingsService(api=api_service, org_id=self._org_id)

    @property
    def name(self) -> str:
        return "query_and_filter_organization_booking_data"

    @property
    def description(self) -> str:
        return """Useful when querying the requested user's organization's booking data with different filtering options. This tool takes in these following arguments in order. But none of them are required if the user want's to get all the booking information.

        booking_status (str): This arg only takes in 'in-progress', 'completed', and 'needs-booking'.
        client_email (str): Needs when querying all the booking requests of a specific client.
        field_agent_email (str): The email of the person who is in charge for the booking request.
        start_data (str): First date of a given date range. Format YYYY-MM-DD.
        end_date (str): Last date of a given date range. Format YYYY-MM-DD."""

    async def tool_func(
        self,
        booking_status: Optional[str] = None,
        client_email: Optional[str] = None,
        field_agent_email: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union[List[Dict[str, Any]], str]:
        """Get the booking information of an organization.
        This method will get all the booking information and send them to the frontend application through socket.io.
        After successfully sending the booking list to the user it will finish up the process as a normal tool.

        Args:
            booking_status (str): A booking status to filter the bookings.
            client_email (str): A client email address to filter the booking request.
            field_agent_email (str): Field agent email address to filter the bookings.
            start_date (str): The starting date of the date range to filter the bookings.
            end_date (str): The ending date of the date range to filter the bookings

        Returns:
            str: Stringified version of the JSON data returned from the server or the error message.
        """
        try:
            result = await self._service.get_bookings(
                date_range={"start_date": start_date, "end_date": end_date},
                status=booking_status,
                client_email=client_email,
                field_agent_email=field_agent_email,
            )
        except Exception as e:
            print(e)
            return f"Unable to get the booking info. Error: {str(e)}"

        reduced_data: List[Dict[str, Any]] = []
        if len(result) > 0:
            for booking in result:
                if not booking.get("id"):
                    continue
                reduced_data.append(
                    {
                        "id": booking.get("id"),
                        "mtNo": booking.get("mtNo"),
                        "createdAt": booking.get("createdAt"),
                        "updatedAt": booking.get("updatedAt"),
                        "jobStatus": booking.get("jobStatus"),
                        "clientName": booking.get("clientName"),
                        "clientPrimaryContact": booking.get("clientPrimaryContact"),
                        # "fieldAgent": booking.get("fieldAgent"),
                        # "booking": booking.get("booking"),
                    }
                )
        return reduced_data
