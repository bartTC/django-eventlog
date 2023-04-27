from django.apps import apps
from django.contrib import admin
from django.template.defaultfilters import timesince_filter
from django.utils.translation import gettext_lazy as _

from eventlog.models import Event

config = apps.get_app_config("eventlog")


class EventAdmin(admin.ModelAdmin):
    """
    Event Admin.
    """

    list_display = (
        "relative_timestamp",
        "group_label",
        "type_display",
        "message",
        "initiator",
    )
    search_fields = ("group", "message", "initiator")
    list_filter = ("type", "timestamp")
    change_list_template = "admin/eventlog/event/change_list.html"
    change_form_template = "admin/eventlog/event/change_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_types = config.get_event_types()

    @admin.display(description="Time")
    def relative_timestamp(self, obj):
        return _("{time} ago").format(time=timesince_filter(obj.timestamp))

    @admin.display(description="Type")
    def type_display(self, obj):
        return obj.type_label

    def get_readonly_fields(self, request, obj=None):
        """All fields are readonly. It's pure logging."""
        return [i.name for i in obj._meta.get_fields()]

    def has_add_permission(self, request):
        """Nobody can add events manually. Only programatically."""
        return False


admin.site.register(Event, EventAdmin)
