from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.contrib import admin
from django.template.defaultfilters import timesince_filter
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .apps import EventLogConfig
    from .models import Event


config: EventLogConfig = apps.get_app_config("eventlog")
event_model: Event = apps.get_model("eventlog", "Event")


def get_difference(obj: Event, next_obj: Event) -> str:
    """
    Calculates the elapsed time between two Event objects.
    Returns a string in the format:

    "1d 4h 7m 0s"
    "4h 7m 0s"
    "5s"
    """
    delay = int((next_obj.timestamp - obj.timestamp).total_seconds())
    years, remainder = divmod(delay, 60 * 60 * 24 * 365)
    days, remainder = divmod(remainder, 60 * 60 * 24)
    hours, remainder = divmod(remainder, 60 * 60)
    mins, secs = divmod(remainder, 60)
    times = {"y": years, "d": days, "h": hours, "m": mins, "s": secs}
    if sum(times.values()) == 0:
        return _("- same time")

    duration = " ".join((f"{value}{key}" for key, value in times.items() if value > 0))
    return _("{duration} later").format(duration=duration)


@admin.register(event_model)
class EventAdmin(admin.ModelAdmin):
    """Event Admin."""

    list_display = (
        "relative_timestamp",
        "__str__",
        "html_label",
        "message",
        "initiator",
    )
    search_fields = ("group", "message", "initiator")
    list_filter = ("type", "timestamp")
    change_list_template = "admin/eventlog/event/change_list.html"
    change_form_template = "admin/eventlog/event/change_form.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.event_types = config.get_event_types()

    @admin.display(description="Time", ordering="timestamp")
    def relative_timestamp(self, obj: Event) -> str:
        return _("{time} ago").format(time=timesince_filter(obj.timestamp))

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Nobody can add events manually. Only programmatically."""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Event | None = None
    ) -> bool:
        """Nobody can change event data."""
        return False

    def render_change_form(
        self,
        request: HttpRequest,
        context: dict[str, Any],
        obj: Event = None,
        **kwargs: Any,
    ) -> HttpResponse:
        """
        Annotate the delay between events.
        """
        if not obj:  # pragma: no cover
            return super().render_change_form(request, context, obj=obj, **kwargs)

        qs = event_model.objects.filter(group=obj.group).order_by("timestamp")

        last = None
        for e in qs:
            if last:
                e.timestamp_delay = get_difference(last, obj)
            last = e
        context["event_list"] = qs
        return super().render_change_form(request, context, **kwargs)
