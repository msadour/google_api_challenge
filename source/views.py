from rest_framework import viewsets
from rest_framework.response import Response

from source.utils.mail import MailManager


class MailViewSet(viewsets.ViewSet):
    """
    Mail viewset.
    """

    mail = MailManager()

    def list(self, request):
        mails = self.mail.retrieve_mail(filter_content=request.query_params)
        return Response(data={"mails": mails})

    def create(self, request):
        to = request.data.get("to")
        subject = request.data.get("subject", "No subject")
        message_text = request.data.get("message_text", "")
        try:
            self.mail.send_email(to, subject, message_text)
        except Exception as e:
            return Response({"message": "Mail not sent", "error": str(e)})
        else:
            return Response({"message": "Mail sent"})
