from __future__ import annotations

from uuid import uuid4

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .datastructures import EventType, EventTypeList


class EventLogConfig(AppConfig):
    name = "eventlog"
    verbose_name = "EventLog"
    default_auto_field = "django.db.models.AutoField"

    # -- List of event types to be used in events.
    event_types: EventTypeList = EventTypeList(
        EventType(name="info", label=_("Info")),
        EventType(name="warning", label=_("Warning")),
        EventType(name="error", label=_("Error"), color="red"),
        EventType(name="critical", label=_("Critical"), color="white", bgcolor="red"),
    )

    # -- Email Notification Settings

    # Fail silently if the email server does not exist or respond
    email_fail_silently: bool = False

    # From email address used when sending notifications
    email_from: str | None = settings.DEFAULT_FROM_EMAIL

    # Email subject and text body templates. This needs to be a standard
    # Python string. You may use 'new style' format variables here.
    #
    # {type} ......: Event type, such as "Info" or "Warning".
    # {date} ......: The date and time the event was triggered.
    # {message} ...: The message sent with the event.
    # {data} ......: The JSON data attached to the event.
    # {initiator} .: The initiator string (optional)
    email_subject_template: str = _("Event Log: {type}")
    email_template: str = _(
        "The Event was {type} on {date}\n\n{message}\n\n-- {initiator}",
    )

    def get_event_types(self) -> EventTypeList:
        """
        All code calls this method and not `self.event_types`, so you can
        programmatically create event types, if required.
        """
        return self.event_types

    def generate_group_id(self) -> str:
        """
        Method to create a new, random group id.
        """
        return uuid4().hex
