from uuid import uuid4

from django.apps import apps
from django.core.mail import send_mail as django_send_mail
from django.utils.html import linebreaks

from eventlog.models import Event as EventModel

config = apps.get_app_config('eventlog')


class EventGroup(object):
    """
    Enterprise Event Object Factory.
    """
    group_id = None
    event_types = None
    send_mail = None

    def __init__(self, send_mail=None):
        self.group_id = uuid4().hex
        self.event_types = config.get_event_types()
        self.send_mail = send_mail

    def __getattr__(self, attr):
        if attr in self.event_types.keys():
            def f(*args, **kwargs):
                print('f:', args, kwargs)
                return self._log_event(attr, *args, **kwargs)
            f.__name__ = attr
            return f
        raise AttributeError('Event type "{}" does not exist'.format(attr))

    def _log_event(self, type, message, initiator=None, send_mail=None):
        """
        Log a new event entry.
        """
        print('called log event with type', type)
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
        context = {
            'type': event_object.get_type_display(),
            'message': event_object.message,
            'initiator': event_object.initiator,
            'date': event_object.timestamp
        }
        subject = config.email_subject_template.format(**context)
        text_message = config.email_template.format(**context)
        html_message = '<html><body>{html}</body></html>'.format(
            html=linebreaks(text_message))

        django_send_mail(
            subject=subject,
            message=text_message,
            html_message=html_message,
            recipient_list=[email],
            from_email=config.email_from,
            fail_silently=config.email_fail_silently
        )
