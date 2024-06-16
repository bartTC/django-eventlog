from __future__ import annotations

import re
from logging import getLogger
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import models
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .datastructures import EventType

if TYPE_CHECKING:
    from .apps import EventLogConfig


logger = getLogger(__name__)
config: EventLogConfig = apps.get_app_config("eventlog")


class Event(models.Model):
    """Event log model."""

    type = models.CharField(_("Event Type"), max_length=50)
    group = models.CharField(_("Event Group"), max_length=40, db_index=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    message = models.TextField(_("Message"))
    data = models.JSONField(_("Data"), blank=True, null=True)
    initiator = models.CharField(  # noqa: DJ001 avoid null=True on CharFields
        _("Initiator"),
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-timestamp",)
        indexes = (
            models.Index(fields=["group", "timestamp"]),
            models.Index(fields=["timestamp"]),
        )
        verbose_name = _("Event Log")
        verbose_name_plural = _("Event Logs")

    def __str__(self) -> str:
        # If this is an UUID, shorten it to the first 8 characters
        if re.match(r"[a-f0-9]{32}", str(self.group)):
            return self.group[:8]
        return str(self.group)

    @property
    @method_decorator(mark_safe)
    def html_label(self) -> str:
        type_name = str(self.type)
        event_types = config.get_event_types()

        # Event type exists in DB, but no longer defined in AppConfig.event_types.
        if not (event_type := event_types.by_name(type_name)):
            event_type = EventType(name=type_name, label=type_name.title())

        return event_type.html_label
