from uuid import uuid4

from django.apps import apps
from django.core.mail import send_mail as django_send_mail
from django.utils.html import linebreaks

def generate_group_id():
    return uuid4().hex

class EventGroup(object):
    """
    Enterprise Event Object Factory.
    """
    group_id = None
    event_types = None
    send_mail = None

    def __init__(self, send_mail=None, group_id=None):
        self.config = apps.get_app_config('eventlog')
        self.group_id = group_id or generate_group_id()
        self.event_types = self.config.get_event_types()
        self.send_mail = send_mail

    def __getattr__(self, attr):
        if attr in self.event_types.keys():
            def f(*args, **kwargs):
                return self._log_event(attr, *args, **kwargs)
            f.__name__ = attr
            return f
        raise AttributeError('Event type "{}" does not exist'.format(attr))

    def _log_event(self, type, message, initiator=None, send_mail=None):
        """
        Log a new event entry.
        """
        EventModel = apps.get_model('eventlog', 'Event')
        event_object = EventModel.objects.create(
            type=type, group=self.group_id, message=message, initiator=initiator)

        # Mail this event per email. Either if this method has it enabled,
        # or if its globally enabled for the EventGroup.
        mail = send_mail or self.send_mail
        if mail:
            self._send_mail(mail, event_object)

    def _send_mail(self, email, event_object):
        """
        Send a simple HTML email to the recipient defined in :email:.
        """
        type_label = self.event_types.get(event_object.type, None)
        if not type_label:
            return event_object.type.capitalize()
        context = {
            'type': type_label,
            'message': event_object.message,
            'initiator': event_object.initiator,
            'date': event_object.timestamp
        }
        subject = self.config.email_subject_template.format(**context)
        text_message = self.config.email_template.format(**context)
        html_message = '<html><body>{html}</body></html>'.format(
            html=linebreaks(text_message))

        django_send_mail(
            subject=subject,
            message=text_message,
            html_message=html_message,
            recipient_list=[email],
            from_email=self.config.email_from,
            fail_silently=self.config.email_fail_silently
        )
