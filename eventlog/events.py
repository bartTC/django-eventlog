from uuid import uuid4

from django.apps import apps
from django.core.mail import send_mail as django_send_mail
from django.utils.html import linebreaks

from eventlog.models import Event as EventModel

config = apps.get_app_config('eventlog')

EventChoices = config.event_type_choices


class Event(object):
    """
    Enterprise Event Object Factory.
    """
    group_id = None

    def __init__(self, type=None, message=None, initiator=None, send_mail=None):
        self.group_id = uuid4().hex
        self.log(type, message, initiator=initiator, send_mail=send_mail)

    def log(self, type=None, message=None, initiator=None, send_mail=None):
        """
        Log a new event entry.
        """
        if not message:
            raise ValueError('A message is required')

        type = type or config.default_event_type
        if not isinstance(type, int):
            type = getattr(EventChoices, type, config.default_event_type)

        event_object = EventModel.objects.create(
            type=type, group=self.group_id, message=message, initiator=initiator)

        if send_mail:
            self.send_mail(send_mail, event_object)

    def send_mail(self, email, event_object):
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
