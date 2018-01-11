from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class EventLogConfig(AppConfig):
    name = 'eventlog'
    verbose_name = 'EventLog'

    email_fail_silently = False
    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject_template = 'Event Log: {type}'
    email_template = _('The Event was {type} on {date}\n\n{message}\n\n-- {initiator}')

    @property
    def event_type_choices(self):
        """
        List of event types to be used in events.
        """
        from model_utils import Choices
        return Choices(
            (1, 'start', _('Started')),
            (2, 'in_progress', _('In Progress')),
            (3, 'done', _('Done')),
            (4, 'single', _('Single Event')),
        )

    @property
    def default_event_type(self):
        """
        The default event type if not provided in an event log.
        """
        return self.event_type_choices.single
