from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class EventLogConfig(AppConfig):
    name = 'eventlog'
    verbose_name = 'EventLog'

    # List of event types to be used in events. A list of dictionaries
    # in the format::
    #
    #     {
    #         'name': 'info',      # The method name.
    #         'label': _('Info'),  # Human readable label
    #         'color': None,       # Foreground Hex color used in the Admin changelist. Optional.
    #         'bgcolor': None,     # Background Hex color used in the Admin changelist. Optional.
    #     }
    #
    # Method names must be lowercase and only contain strings, numbers and
    # underscores, but must not start with either a number or underscore.
    # The max length is 50 characters.
    #
    # This is OK:  yolo, hello_world, jerry123
    # This is NOK: _yolo, 1pineappleplease,
    event_types = {
            'info': {
                'label': _('Info'),
                'color': None,
                'bgcolor': None,
            },
            'warning': {
                'label': _('Warning'),
                'color': None,
                'bgcolor': None,
            },
            'error': {
                'label': _('Error'),
                'color': 'red',
                'bgcolor': None,
            },
            'critical': {
                'label': _('Critical'),
                'color': 'white',
                'bgcolor': 'red',
            },
        }


    # -- Email Notification Settings

    # Fail silently if the email server does not exist or respond
    email_fail_silently = False

    # From email address used when sending notifications
    email_from = settings.DEFAULT_FROM_EMAIL

    # Email subject and text body templates. This needs to be a standard
    # Python string. You may use 'new style' format variables here.
    #
    # {type}      Event type, such as "Info" or "Warning".
    # {date}      The date and time the event was triggered.
    # {message}   The message sent with the event.
    # {initiator} The initiator string (optional)
    email_subject_template = _('Event Log: {type}')
    email_template = _('The Event was {type} on {date}\n\n{message}\n\n-- {initiator}')

    def get_event_types(self):
        """
        All code calls this method and not `self.event_types`, so you can
        programmatically create event types, if required..
        """
        return self.event_types
