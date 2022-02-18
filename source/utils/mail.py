"""Mail module."""

import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from source.utils.constants import EMAIL
from source.utils.google import create_service


class MailManager:
    def __init__(self):
        self.service = create_service()

    def send_email(self, payload):
        """Create a message for an email.

        Args:
          payload:

        Returns:
          An object containing a base64url encoded email object.
        """
        try:
            to = payload.data.get("to")
            subject = payload.data.get("subject", "No subject")
            message_text = payload.data.get("message_text", "")

            email_message = message_text
            mime_message = MIMEMultipart()
            mime_message["to"] = to
            mime_message["from"] = EMAIL
            mime_message["subject"] = subject
            mime_message.attach(MIMEText(email_message, "plain"))
            raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
            self.service.users().messages().send(
                userId="me", body={"raw": raw_string}
            ).execute()
        except Exception:
            return "Mail not sent"
        else:
            return "Mail sent"

    def retrieve_mail(self, filter_content=None):
        all_messages = []
        result = self.service.users().messages().list(userId="me").execute()
        messages = result.get("messages")
        for msg in messages:
            txt = (
                self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            )
            try:
                payload = txt["payload"]
                headers = payload["headers"]

                subject = "No subject"
                sender = None
                for d in headers:
                    if d["name"] == "Subject":
                        subject = d["value"]
                    if d["name"] == "From":
                        sender = d["value"]

                parts = payload.get("parts")[0]
                data = parts["body"]["data"]
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = (
                    base64.b64decode(data).decode("ascii").replace("\r\n", "")
                )

                if decoded_data and sender:
                    if not filter_content:
                        message = {
                            "Subject": subject,
                            "From": sender,
                            "Message": decoded_data,
                        }
                        all_messages.append(message)
                    else:
                        if (
                            filter_content["search"] in decoded_data
                            or filter_content["search"] in sender
                            or filter_content["search"] in subject
                        ):
                            message = {
                                "Subject": subject,
                                "From": sender,
                                "Message": decoded_data,
                            }
                            all_messages.append(message)
            except:
                pass
        return all_messages
