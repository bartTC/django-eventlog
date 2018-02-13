from datetime import datetime, timedelta
from logging import getLogger
import re

from django.apps import apps
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext_lazy

logger = getLogger(__file__)
config = apps.get_app_config('eventlog')


class EventLogManager(models.Manager):
    def purge(self, days=30):
        """
        Delete all events older than <days> days.
        """
        return self.filter(
            timestamp__gt=datetime.now() - timedelta(days=days)
        ).delete()


class Event(models.Model):
    """
    Event log model.
    """
    type = models.CharField(_('Event Type'), max_length=50)
    group = models.UUIDField(_('Event Group'))
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    message = models.CharField(_('Message'), max_length=500)
    initiator = models.CharField(_('Initiator'), max_length=500, blank=True, null=True)

    objects = EventLogManager()

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _('Event Log')
        verbose_name_plural = _('Event Logs')

    def __str__(self):
        return '{group} - {type} - {message}...'.format(
            group=self.group_label,
            type=self.type,
            message=self.message[:40])

    @property
    def group_label(self):
        return self.group.hex[-6:]

    @property
    def type_label(self):
        event_types = config.get_event_types()
        label = event_types.get(self.type, None)
        if not label:
            return self.type.capitalize()
        s = '<span class="eventType" style="{color} {bgcolor}">{label}</span>'.format(
            color='color: {0};'.format(label['color']) if label.get('color', None) else '',
            bgcolor='background-color: {0};'.format(label['bgcolor']) if label.get('bgcolor', None) else '',
            label=label['label'])
        return mark_safe(s)

    def get_all_group_events(self):
        """
        Get all events which are in the same Event group as this event.
        """
        qs = Event.objects.filter(group=self.group).order_by('timestamp')
        # Annotate the delay between events
        last = None
        for e in qs:
            if last:
                delay = int((e.timestamp - last.timestamp).total_seconds())
                delay_minutes, delayseconds = divmod(delay, 60)
                e.timestamp_delay = ugettext_lazy('{min}m {sec}s').format(
                    min=delay_minutes, sec=delayseconds
                )
            last = e
        return qs
