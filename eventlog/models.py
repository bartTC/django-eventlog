from __future__ import annotations

from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = getLogger(__file__)
config = apps.get_app_config("eventlog")


class EventLogManager(models.Manager):
    def purge(self, days: int = 30) -> QuerySet:
        """Delete all events older than <days> days."""
        return self.filter(
            timestamp__gt=datetime.now(tz=timezone.UTC) - timedelta(days=days),
        ).delete()


class Event(models.Model):
    """Event log model."""

    type = models.CharField(  # noqa: A003 `type` is shadowing a python builtin
        _("Event Type"),
        max_length=50,
    )
    group = models.CharField(_("Event Group"), max_length=40)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    message = models.TextField(_("Message"))
    initiator = models.CharField(  # noqa: DJ001
        _("Initiator"),
        max_length=500,
        blank=True,
        null=True,
    )

    objects = EventLogManager()

    class Meta:
        ordering = ("-timestamp",)
        indexes = [
                models.Index(fields=["group", "timestamp"]),
                models.Index(fields=["timestamp"]),
        ]
        verbose_name = _("Event Log")
        verbose_name_plural = _("Event Logs")

    def __str__(self) -> str:
        return "{group} - {type} - {message}...".format(
            group=self.group_label,
            type=self.type,
            message=self.message[:40],
        )

    @property
    def group_label(self) -> str:
        return self.group

    @property
    def type_label(self) -> str:
        event_types = config.get_event_types()
        label = event_types.get(self.type, None)

        if not label:
            return self.type.capitalize()
        # fmt: off
        s = '<span class="eventType" style="{color} {bgcolor}">{label}</span>'.format(
            color="color: {};".format(label["color"]) if label.get("color", None) else "",
            bgcolor="background-color: {};".format(label["bgcolor"]) if label.get("bgcolor", None) else "",
            label=label["label"],
        )
        # fmt: on
        return mark_safe(s)  # noqa: S308 mark_safe

    def get_all_group_events(self) -> QuerySet:
        """Get all events that are in the same Event group as this event."""
        qs = Event.objects.filter(group=self.group).order_by("timestamp")
        # Annotate the delay between events
        last = None
        for e in qs:
            if last:
                delay = int((e.timestamp - last.timestamp).total_seconds())
                delay_minutes, delayseconds = divmod(delay, 60)
                e.timestamp_delay = _("{min}m {sec}s").format(
                    min=delay_minutes,
                    sec=delayseconds,
                )
            last = e
        return qs
