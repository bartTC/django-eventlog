from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Callable
from uuid import uuid4

from django.apps import apps
from django.core.mail import send_mail as django_send_mail
from django.utils.html import linebreaks

if TYPE_CHECKING:
    from django.db.models import Model


def generate_group_id() -> str:
    return uuid4().hex


class EventGroup:
    """Enterprise Event Object Factory."""

    event_model: type[Model] = NotImplemented
    group_id: str = NotImplemented
    event_types: dict = NotImplemented
    send_mail: str | None = None

    def __init__(
        self,
        send_mail: str | None = None,
        group_id: str | None = None,
    ) -> None:
        self.event_model = apps.get_model("eventlog", "Event")
        self.config = apps.get_app_config("eventlog")
        self.group_id = group_id or generate_group_id()
        self.event_types = self.config.get_event_types()
        self.send_mail = send_mail

    def __getattr__(self, attr: str) -> Callable:
        if attr in self.event_types:

            def f(*args: Any, **kwargs: Any) -> None:
                return self._log_event(attr, *args, **kwargs)

            f.__name__ = attr
            return f
        err = f'Event type "{attr}" does not exist'
        raise AttributeError(err)

    def _log_event(  # noqa: PLR0913 Too many arguments
        self,
        event_type: str,
        message: str,
        initiator: str | None = None,
        send_mail: str | None = None,
        data: Any | None = None,
    ) -> None:
        """Log a new event entry."""

        # Make sure, the data is JSON serizable, otherwise store it as a string.
        if data:
            try:
                json.dumps(data)
            except TypeError:
                data = str(data)

        event_object = self.event_model.objects.create(
            type=event_type,
            group=self.group_id,
            message=message,
            data=data,
            initiator=initiator,
        )

        # Mail this event per email. Either if this method has it enabled,
        # or if its globally enabled for the EventGroup.
        mail = send_mail or self.send_mail
        if mail:
            self._send_mail(mail, event_object)

    def _send_mail(self, email: str, event_object: event_model) -> None:
        """Send a simple HTML email to the recipient defined in :email:."""
        type_label = self.event_types.get(event_object.type, None)
        if not type_label:
            return event_object.type.capitalize()
        context = {
            "type": type_label,
            "message": event_object.message,
            "data": event_object.data,
            "initiator": event_object.initiator,
            "date": event_object.timestamp,
        }
        subject = self.config.email_subject_template.format(**context)
        text_message = self.config.email_template.format(**context)
        html_message = f"<html><body>{linebreaks(text_message)}</body></html>"

        django_send_mail(
            subject=subject,
            message=text_message,
            html_message=html_message,
            recipient_list=[email],
            from_email=self.config.email_from,
            fail_silently=self.config.email_fail_silently,
        )
        return None
