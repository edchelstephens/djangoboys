from django.conf import settings
from mail_templated import send_mail


class EmailMixin:
    """Email mixin."""

    def get_default_from_email(self) -> str:
        """Get default from email."""
        return settings.DEFAULT_FROM_EMAIL

    def send_templated_mail(
        self,
        template_name: str,
        context: dict,
        send_to: str,
        from_email: str | None = settings.DEFAULT_FROM_EMAIL,
        **kwargs
    ) -> int:
        """Send templated mail and return count of sent messages."""
        recipient_list = [send_to]
        return send_mail(
            template_name=template_name,
            context=context,
            from_email=from_email,
            recipient_list=recipient_list,
            **kwargs
        )
