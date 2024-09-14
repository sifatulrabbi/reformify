import httpx
import json
from socketio import AsyncServer
from typing import Dict, Callable, Union, Any, List
from icecream import ic
from configs import XBOOKER_API_URL, XBOOKER_INTERNAL_API_KEY


class SimpleXAgentTools:
    """Simple agent tools."""

    def __init__(self, sio: AsyncServer):
        self._sio = sio

    @property
    def tools_map(self) -> Dict[str, Callable[[Dict[str, str]], str]]:
        return {
            "send_booking_invitation": self._send_booking_invitation,
            "get_organization_booking_list": self._get_organization_booking_info,
        }

    @property
    def available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "send_booking_invitation",
                "description": "useful when sending booking invitation to an email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_email": {
                            "type": "string",
                            "description": "Email of the client who will receive the booking invitation",
                        },
                        "discount": {
                            "type": "number",
                            "description": "Discount amount in a float format, for example 10% discount will be 0.1",
                        },
                    },
                    "required": ["client_email"],
                },
            },
            {
                "name": "get_organization_booking_list",
                "description": "Useful when getting the booking list of the user's organization, and also filtering booking information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["in-progress", "completed", "needs-booking"],
                            "description": "current status of a booking request that will be used to filter booking requests by status",
                        },
                        "client_email": {
                            "type": "string",
                            "description": "email address used to filter booking requests by a specific client.",
                        },
                        "field_agent_email": {
                            "type": "string",
                            "description": "Email address used to filter booking requests by the field agent who is handling the booking request.",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date of the date range by which the booking requests will be filtered. Use 'today' if the user wants to get bookings of the current day. The date format is 'YYYY-MM-DD'.",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date of the date range by which the booking requests will be filtered. If there are no end date specified then the default end date is 'today'. The date format is 'YYYY-MM-DD'.",
                        },
                    },
                    "required": [],
                },
            },
        ]

    def _send_booking_invitation(
        self, args: Dict[str, str], user_session: Dict[str, Union[str, Dict]]
    ) -> str:
        """Send a booking invitation to the specified email address.

        Args:
            args (Dict[str, str]): The arguments provided by the agent.
            user_session (Dict[str, Union[str, Dict]]): Current user's session info.

        Returns:
            dict: Final result
        """
        org_id = user_session.get("organization").get("id")
        user_id = user_session.get("id")
        user_name = user_session.get("fullname")
        client_email = args.get("client_email")
        discount = args.get("discount")
        # verify the args provided by the agent.
        if not org_id:
            return "No organization's id found in the current session."
        if not user_id:
            return "User's id not found in the current session."
        if not client_email:
            return "client_email wasn't specified in the request payload."

        try:
            url = f"{XBOOKER_API_URL}/api/v1/instructions/{org_id}/bookingInvitation"
            headers = {"X-Booker-Api-Key": XBOOKER_INTERNAL_API_KEY}
            payload = {
                "clientEmail": client_email,
                "discount": discount,
                "user_id": user_id,
                "user_name": user_name if user_name else "",
            }
            r = httpx.post(url, headers=headers, json=payload)
            if r.status_code != httpx.codes.CREATED:
                data: Dict[str, str] = r.json()
                return data.get("error")
            return "The booking invitation was sent successfully"
        except Exception as e:
            return str(e)

    def _get_organization_booking_info(
        self, args: Dict[str, str], user_session: Dict[str, Any]
    ):
        """Get the booking information of an organization.
        This method will get all the booking information and send them to the frontend application through socket.io.
        After successfully sending the booking list to the user it will finish up the process as a normal tool.

        Args
            args (Dict[str, str]): The arguments provided by the agent.
            user_session (Dict[str, str]): The current user's session.

        Returns:
            str: A success message or the error message.
        """
        status: Union[str, None] = args.get("status")
        client_email: Union[str, None] = args.get("client_email")
        field_agent_email: Union[str, None] = args.get("field_agent_email")
        start_date: Union[str, None] = args.get("start_date")
        end_date: Union[str, None] = args.get("end_date")
        org_id: str = user_session.get("organization").get("id")
        user_id: str = user_session.get("id")
        try:
            ic(args)
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "clientEmail": client_email,
                "status": status,
                "fieldAgentEmail": field_agent_email,
            }
            headers = {"X-Booker-Api-Key": XBOOKER_INTERNAL_API_KEY}
            r = httpx.get(
                f"{XBOOKER_API_URL}/api/v1/instructions/{org_id}/list",
                headers=headers,
                params=params,
            )
            results = r.json()
            reduced_data = []
            if results.get("data") and len(results.get("data")) > 0:
                for booking in results.get("data"):
                    reduced_data.append(
                        {
                            "mtNo": booking.get("mtNo"),
                            "createdAt": booking.get("createdAt"),
                            "updatedAt": booking.get("updatedAt"),
                            "jobStatus": booking.get("jobStatus"),
                            "clientName": booking.get("clientName"),
                            "clientPrimaryContact": booking.get("clientPrimaryContact"),
                            "fieldAgent": booking.get("fieldAgent"),
                            "booking": booking.get("booking"),
                        }
                    )
            ic(reduced_data)
            return json.dumps(reduced_data)
            # return "The requested booking list is already sent to the user."
        except Exception as e:
            return json.dumps({"error": str(e), "success": False})

    def _get_organization_todolist_info(
        self, args: Dict[str, Any], user_session: Dict[str, Any]
    ):
        """Get todo list information of the current organization.

        Args:
            args (Dict[str, Any]): The arguments provided by the agent.
            user_session (Dict[str, str]): The current user's session.

        Returns:
            str: A success message or the error message.
        """
        org_id: str = user_session.get("organization").get("id")
        user_id: str = user_session.get("id")
        try:
            ic(args)
            headers = {"X-Booker-Api-Key": XBOOKER_INTERNAL_API_KEY}
            params = {}
            r = httpx.get(
                f"{XBOOKER_API_URL}/api/v1/todos/{org_id}/list",
                headers=headers,
                params=params,
            )
            return "The requested todos list is already sent to the user."
        except Exception as e:
            return str(e)
