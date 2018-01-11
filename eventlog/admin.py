from django.contrib import admin
from django.template.defaultfilters import timesince_filter
from django.utils.translation import ugettext_lazy as _

from eventlog.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('relative_timestamp', 'group_label', 'type_display',
                    'message', 'initiator')
    search_fields = ('group', 'message', 'initiator')
    list_filter = ('type', 'timestamp')
    change_list_template = 'admin/eventlog/event/change_list.html'

    def relative_timestamp(self, obj):
        return _('{time} ago').format(time=timesince_filter(obj.timestamp))
    relative_timestamp.short_description = 'Time'

    def type_display(self, obj):
        return obj.get_type_display()
    type_display.short_description = 'Type'
