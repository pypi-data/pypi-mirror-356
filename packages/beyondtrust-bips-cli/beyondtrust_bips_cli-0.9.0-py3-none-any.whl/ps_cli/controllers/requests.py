from secrets_safe_library import exceptions, requests
from secrets_safe_library.constants.endpoints import (
    GET_REQUESTS,
    POST_REQUESTS,
    POST_REQUESTS_ALIASES,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.requests import fields as requests_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Request(CLIController):
    """
    Works with Secrets Safe Requests - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="requests",
            help="requests management commands",
        )

    @property
    def class_object(self) -> requests.Request:
        if self._class_object is None and self.app is not None:
            self._class_object = requests.Request(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    @option(
        "-s",
        "--status",
        help="The Request status. Options: all, pending, active",
        type=str,
        required=False,
        default="all",
    )
    @option(
        "-q",
        "--queue",
        help="The Request queue. Options: req, app",
        type=str,
        required=False,
        default="req",
    )
    def list_requests(self, args):
        """
        Returns a list of Requests to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_REQUESTS, requests_fields, Version.DEFAULT)
            self.display.v("Calling list_requests function")
            requests_list = self.class_object.get_requests(
                status=args.status, queue=args.queue
            )
            self.display.show(requests_list, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list requests")

    @command
    @aliases("create")
    @option(
        "-s-id ",
        "--system-id",
        help="The Managed System id",
        type=int,
        required=True,
    )
    @option(
        "-a-id",
        "--account-id",
        help="The Managed Account id",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration in minutes",
        type=int,
        required=True,
    )
    @option(
        "-app-id",
        "--application-id",
        help="The application id",
        type=int,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the request",
        type=str,
        required=False,
    )
    @option(
        "-a-type",
        "--access-type",
        help="The access type. Options: View, RDP, SSH, App",
        type=str,
        required=False,
    )
    @option(
        "-a-p-id",
        "--access-policy-schedule-id",
        help="The access policy schedule id",
        type=int,
        required=False,
    )
    @option(
        "-c-op",
        "--conflict-option",
        help="The conflict option",
        type=str,
        required=False,
    )
    @option(
        "-t-sys-id",
        "--ticket-system-id",
        help="The ticket system id",
        type=int,
        required=False,
    )
    @option(
        "-t-num",
        "--ticket-number",
        help="Ticket number associated with the request",
        type=str,
        required=False,
    )
    @option(
        "-r-o-c",
        "--rotate-on-checkin",
        help="Rotate on checkin",
        type=bool,
        required=False,
    )
    def create_request(self, args):
        """
        Creates a new Request.
        """
        try:
            fields = self.get_fields(POST_REQUESTS, requests_fields, Version.DEFAULT)
            self.display.v("Calling create_request function")
            request = self.class_object.post_request(
                system_id=args.system_id,
                account_id=args.account_id,
                duration_minutes=args.duration_minutes,
                application_id=args.application_id,
                reason=args.reason,
                access_type=args.access_type,
                access_policy_schedule_id=args.access_policy_schedule_id,
                conflict_option=args.conflict_option,
                ticket_system_id=args.ticket_system_id,
                ticket_number=args.ticket_number,
                rotate_on_checkin=args.rotate_on_checkin,
            )
            self.display.show(request, fields)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it("It was not possible to create request")
            print_it(f"Error: {e}")

    @command
    @option(
        "-a-id",
        "--alias-id",
        help="ID of the managed account alias.",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration in minutes",
        type=int,
        required=True,
    )
    @option(
        "-acc-t",
        "--access-type",
        help="The access type. Options: View, RDP, SSH, App",
        type=str,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the request",
        type=str,
        required=False,
    )
    @option(
        "-a-p-id",
        "--access-policy-schedule-id",
        help="The access policy schedule id",
        type=int,
        required=False,
    )
    @option(
        "-c-op",
        "--conflict-option",
        help="The conflict option",
        type=str,
        required=False,
    )
    @option(
        "-t-sys-id",
        "--ticket-system-id",
        help="The ticket system id",
        type=int,
        required=False,
    )
    @option(
        "-t-num",
        "--ticket-number",
        help="Ticket number associated with the request",
        type=str,
        required=False,
    )
    @option(
        "-r-o-c",
        "--rotate-on-checkin",
        help="Rotate on checkin",
        type=bool,
        required=False,
    )
    def create_request_alias(self, args):
        """
        Creates a new release request using an alias.
        """
        try:
            fields = self.get_fields(
                POST_REQUESTS_ALIASES, requests_fields, Version.DEFAULT
            )
            self.display.v("Calling create_request function")
            request = self.class_object.post_request_alias(
                alias_id=args.alias_id,
                duration_minutes=args.duration_minutes,
                access_type=args.access_type,
                reason=args.reason,
                access_policy_schedule_id=args.access_policy_schedule_id,
                conflict_option=args.conflict_option,
                ticket_system_id=args.ticket_system_id,
                ticket_number=args.ticket_number,
                rotate_on_checkin=args.rotate_on_checkin,
            )
            self.display.show(request, fields)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create request")
            print_it(f"Error: {e}")

    @command
    @aliases("checkin-request")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the check-in",
        type=str,
        required=False,
    )
    def put_request_checkin(self, args):
        """
        Check-in a Request.
        """
        try:
            self.display.v("Calling post_request_checkin function")
            self.class_object.put_request_checkin(
                request_id=args.request_id, reason=args.reason
            )
            print_it(f"Request with ID {args.request_id} was checked-in successfully")
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to check-in request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("approve-request")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the approval",
        type=str,
        required=False,
    )
    def put_request_approve(self, args):
        """
        Approve a Request.
        """
        try:
            self.display.v("Calling put_request_approve function")
            self.class_object.put_request_approve(
                request_id=args.request_id, reason=args.reason
            )
            print_it(f"Request with ID {args.request_id} was approved successfully")
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to approve request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("deny")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the denial",
        type=str,
        required=False,
    )
    def put_request_deny(self, args):
        """
        Deny a Request.
        """
        try:
            self.display.v("Calling put_request_deny function")
            self.class_object.put_request_deny(
                request_id=args.request_id, reason=args.reason
            )
            print_it(f"Request with ID {args.request_id} was denied successfully")
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it("It was not possible to deny request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("rotate-on-checkin")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    def request_rotate_on_checkin(self, args):
        """
        Updates a request to rotate the credentials on check-in/expiry.
        """
        try:
            self.display.v("Calling put_request_rotate_on_checkin function")
            self.class_object.put_request_rotate_on_checkin(request_id=args.request_id)
            print_it(f"Request with ID {args.request_id} was rotated successfully")
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it("It was not possible to rotate on check-in request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")
