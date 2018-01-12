.. image:: https://travis-ci.org/bartTC/django-eventlog.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-eventlog

.. image:: https://codecov.io/github/bartTC/django-eventlog/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-eventlog?branch=master

===============
django-eventlog
===============

django-eventlog is a very simple Event logger you can use to track certain
events in your code. Events are stored in a Django model and can be viewed
in the Django Admin.

Events can be grouped in a "Event Group" and when hovering over one item
in the admin, all events of the same group are highlighted.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png
   :scale: 100 %

While looking similar, it's not intended to be a replacement for your regular
Python ``logging`` facility, rather an addition to it.

My intention was that users with no access to regular log files can see the
progress and success of certain events. I use it primarily in Task Queues
like Celery_ to inform staff user about the state of background tasks.

django-eventlog stores it's data in a regular database model, so each log entry
will trigger a SQL Insert. Therefore you should be careful using it in high
performance and/or high volume environments.

Installation
============

Install django-eventlog via pip[env] as usual from Pypi.

.. code-block:: bash

    $ pip install django-eventlog

Then add ``eventlog.apps.EventLogConfig`` to your ``INSTALLED_APPS``
setting and migrate the database as usual.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'eventlog.apps.EventLogConfig',
    ]

If you're using Django 1.8 or earlier 😳 you can use the ``eventlog`` app
name here instead of the ``EventLogConfig``. But you won't be able to set
custom event types.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'eventlog',
    ]

Usage
=====

A new Event group is started by the ``EventGroup`` object, which you can call
with individual "types" similar to logging levels in Python logging.

See this example where I create two event entries in an arbitrary task
function:

.. code-block:: python

    from eventlog.events import EventGroup

    # Start a new Event group
    e = EventGroup()
    e.info('Starting to send 100000 emails to all users.', initiator='Mail Sender')
    # ... sending 100000 totally not spam emails...
    e.info('All emails sent!', initiator='Mail Sender')


Each event will show up in the Django Admin changelog view. If you hover over
one, it will highlight all related events as well.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png
   :scale: 100 %

Event types are pre-defined in django-eventlog, but you can define your own
(see below). You can use them to distinct your events and also filter them in
the admin view later. For example to only see ``error`` events.
Currently these event types are defined:

- ``info``
- ``warning``
- ``error``
- ``critical``


Email notification
------------------

You can notify yourself via email by adding the ``send_mail`` argument
to a log call.

.. code-block:: python

    e = EventGroup()
    e.info('Conquered the world!', initiator='The cat',
          send_mail='the-cat@example.com')

You can also pass ``send_mail`` to the ``EventGroup`` class. This way it's
globally enabled for all events of this group.


.. code-block:: python

    e = EventGroup(send_mail='the-cat@example.com')
    e.info('This will send one email.')
    e.info('This will send one email as well.')


[WIP] ``@eventlog`` decorator
-----------------------------

If you want to keep track of function calls you can use the simpler ``eventlog``
decorator. This will add an Event log entry every time the ``contact_view`` view
is called:

.. code-block:: python

    from eventlog.decorators import eventlog

    @eventlog(message='Someone looked at the Contacts page!')
    def contact_view(request, *args, **kwargs):
        return render(...)

Settings
========

I decided to not provide a battery of Settings with this app and rather keep
everything that needs adjustments in the `AppConfig`_. This is a feature
introduced in Django 1.9 and allows you to set settings more programmatically.

Custom type choices
-------------------

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

Tests
=====

Run the testsuite in your local environment using::

    $ cd django-eventlog/
    $ pipenv intall --dev
    $ ./runtests.py

Or use tox to test against various Django and Python versions::

    $ tox -r


You can also invoke the test suite or other 'manage.py' commands by calling
the ``django-admin`` tool with the test app settings::

    $ cd django-eventlog/
    $ pipenv install --dev
    $ DJANGO_SETTINGS_MODULE=eventlog.tests.testapp.settings pipenv run django-admin
    $ DJANGO_SETTINGS_MODULE=eventlog.tests.testapp.settings pipenv run django-admin test
    $ DJANGO_SETTINGS_MODULE=eventlog.tests.testapp.settings pipenv run django-admin makemigrations --dry-run

.. _AppConfig: https://docs.djangoproject.com/en/1.9/ref/applications/
.. _Celery: http://www.celeryproject.org/
.. _EventLogConfig: https://github.com/bartTC/django-eventlog/blob/master/eventlog/apps.py
