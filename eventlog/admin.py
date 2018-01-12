from django.apps import apps
from django.contrib import admin
from django.template.defaultfilters import timesince_filter
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from eventlog.models import Event

config = apps.get_app_config('eventlog')


class EventAdmin(admin.ModelAdmin):
    """
    Event Admin.
    """
    list_display = ('relative_timestamp', 'group_label', 'type_display',
                    'message', 'initiator')
    search_fields = ('group', 'message', 'initiator')
    list_filter = ('type', 'timestamp')
    change_list_template = 'admin/eventlog/event/change_list.html'

    def __init__(self, *args, **kwargs):
        super(EventAdmin, self).__init__(*args, **kwargs)
        self.event_types = config.get_event_types()

    def relative_timestamp(self, obj):
        return _('{time} ago').format(time=timesince_filter(obj.timestamp))
    relative_timestamp.short_description = 'Time'

    def type_display(self, obj):
        t = self.event_types.get(obj.type, None)
        if not t:
            return obj.type.capitalize()
        s = '<span style="{color} {bgcolor}">{label}</span>'.format(
            color='color: {0};'.format(t['color']) if t.get('color', None) else '',
            bgcolor='padding: 1px 4px; background-color: {0};'.format(t['bgcolor']) if t.get('bgcolor', None) else '',
            label=t['label'])
        return mark_safe(s)

    type_display.short_description = 'Type'

admin.site.register(Event, EventAdmin)
