# Settings and Configuration

All configuration is done by customizing the [AppConfig]. This is a feature introduced 
in Django 1.9 and allows you to set settings more programmatically.

Custom Event Types
------------------

By default, django-eventlog comes with some default types, but you can override them in 
a custom Django AppConfig object:

```python
# myproject/apps.py
from django.utils.translation import gettext_lazy as _

from eventlog.apps import EventLogConfig
from eventlog.datastructures import EventType, EventTypeList

class CustomEventLogConfig(EventLogConfig):
    event_types: EventTypeList = EventTypeList(
        EventType(name="info", label=_("Info")),
        EventType(name="oh_crap", label=_("Oh Crap!"), color="red"),
        EventType(name="mail_system", label=_("Mail System"), color="blue"),
    )


# settings.py
INSTALLED_APPS = [
    # Use your custom Config instead of `eventlog.apps.EventLogConfig`
    'myproject.CustomEventLogConfig',
]


# In your code
from eventlog import EventGroup

e = EventGroup()
e.info('Hello World.')
e.oh_crap('Some bad happened')
e.mail_system('Mail sent successfully!')
```

There are much more settings to override, take a look at the [EventLogConfig].

[AppConfig]: https://docs.djangoproject.com/en/1.9/ref/applications/
[EventLogConfig]: https://github.com/bartTC/django-eventlog/blob/master/eventlog/apps.py
