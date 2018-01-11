from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _



class EventLogConfig(AppConfig):
    name = 'eventlog'
    verbose_name = 'EventLog'

    @property
    def event_type_choices(self):
        """
        List of event types to be used in events.\
        """
        from model_utils import Choices
        return Choices(
            (1, 'started', _('Started')),
            (2, 'in_progress', _('In Progress')),
            (3, 'done', _('Done')),
        )
