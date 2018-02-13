.. _settings:

==========================
Settings and Configuration
==========================

I decided to not provide a battery of Settings with this app and rather keep
everything that needs adjustments in the `AppConfig`_. This is a feature
introduced in Django 1.9 and allows you to set settings more programmatically.

Custom Event Types
------------------

By default, django-eventlog comes with some default types, but you can override
them in a custom Django AppConfig object:

.. code-block:: python

    # myproject/apps.py
    from django.utils.translation import ugettext_lazy as _
    from eventlog.apps import EventLogConfig

    class CustomEventLogConfig(EventLogConfig):
        def get_event_types(self):
            return {
                'info': {
                    'label': _('Info'),
                    'color': None,
                    'bgcolor': None,
                },
                'oh_crap': {
                    'label': _('Oh Crap!'),
                    'color': 'red',
                    'bgcolor': None,
                },
                'mail_system': {
                    'label': _('Mail System'),
                    'color': 'blue',
                    'bgcolor': None,
                },
            }


    # settings.py
    INSTALLED_APPS = [
        # Use your custom Config instead of ``eventlog.apps.EventLogConfig``
        'myproject.CustomEventLogConfig',
    ]

    # In your code
    e = EventGroup()
    e.info('Hello World.')
    e.oh_crap('Some bad happened')
    e.mail_system('Mail sent successfully!')

There are much more settings to override, take a look at the EventLogConfig_.

.. _AppConfig: https://docs.djangoproject.com/en/1.9/ref/applications/
.. _EventLogConfig: https://github.com/bartTC/django-eventlog/blob/master/eventlog/apps.py
