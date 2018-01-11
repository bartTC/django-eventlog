from django.apps import apps


EventChoices = apps.get_app_config('eventlog').event_type_choices

class Event(object):
    pass


