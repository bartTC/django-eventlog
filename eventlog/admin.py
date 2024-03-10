from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.contrib import admin
from django.template.defaultfilters import timesince_filter
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .models import Event


config = apps.get_app_config("eventlog")
event_model: Event = apps.get_model("eventlog", "Event")


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
    def relative_timestamp(self, obj: event_model) -> str:
        return _("{time} ago").format(time=timesince_filter(obj.timestamp))

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Nobody can add events manually. Only programmatically."""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: event_model | None = None
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

        qs = event_model.objects.filter(group=obj.group).order_by("timestamp")

        last = None
        for e in qs:
            if last:
                delay = int((e.timestamp - last.timestamp).total_seconds())
                days, remainder = divmod(delay, 60 * 60 * 24)
                hours, remainder = divmod(remainder, 60 * 60)
                mins, secs = divmod(remainder, 60)
                times = {"days": days, "hours": hours, "min": mins, "sec": secs}
                if days:
                    e.timestamp_delay = _("{days}d {hours}h {min}m {sec}s").format(
                        **times
                    )
                elif hours:
                    e.timestamp_delay = _("{hours}h {min}m {sec}s").format(**times)
                else:
                    e.timestamp_delay = _("{min}m {sec}s").format(**times)
            last = e
        context["event_list"] = qs
        return super().render_change_form(request, context, **kwargs)
