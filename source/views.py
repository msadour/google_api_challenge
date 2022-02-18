"""Views module."""

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from source.utils.mail import MailManager


class MailViewSet(viewsets.ViewSet):
    """
    Mail viewset.
    """

    mail = MailManager()

    def list(self, request: Request) -> Response:
        """Retrieve mail(s).

        Args:
          request:

        Returns:
          Response with mails.
        """
        mails = self.mail.retrieve_mail(filter_content=request.query_params)
        return Response(data={"mails": mails})

    def create(self, request: Request) -> Response:
        """Send an email.

        Args:
          request:

        Returns:
          Response with message who say if it sent or not.
        """
        result = self.mail.send_email(payload=request)
        return Response({"message": result})
