from django.core import mail
from django.core.mail import EmailMessage

from tests.testing_utils.parsers import StringToHTMLParserMixin


class EmailTestMixin(StringToHTMLParserMixin):
    """Mixin for tests including sending emails and outbox checking."""

    def get_mail_outbox(self) -> list[EmailMessage]:
        """Get the mail outobox."""
        return mail.outbox

    def get_outbox_receivers(self) -> list[str]:
        """Get list of email outbox receivers"""

        outbox = self.get_mail_outbox()
        email_receivers = []
        for sent_email in outbox:
            recipients = sent_email.to
            email_receivers.extend(recipients)

        return email_receivers

    def get_first_sent_message(self) -> EmailMessage:
        """Get the first sent message on the mail outbox."""
        outbox = mail.outbox
        sent_message = outbox[0]

        return sent_message

    def assertSentMailSubjectEquals(
        self, sent_message: EmailMessage, subject: str, msg: str | None = None
    ) -> None:
        """Assert that sent_mesage.subject stripped is equal to subject string."""

        sent_message_subject = sent_message.subject.strip()
        if msg is None:
            msg = f"'{sent_message_subject}' != '{subject}'"
        assert sent_message_subject == subject, msg

    def assertStringIsInMessageBody(
        self, sent_message: EmailMessage, string: str, msg: str | None = None
    ) -> None:
        """Assert that string is in the message body."""
        string = self.parse_to_html(string)
        message_body = str(sent_message.body)
        if msg is None:
            msg = f"{string} not in {message_body}"
        assert string in message_body, msg
