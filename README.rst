.. image:: https://travis-ci.org/bartTC/django-eventlog.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-eventlog

.. image:: https://codecov.io/github/bartTC/django-eventlog/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-eventlog?branch=master

===============
django-eventlog
===============

django-eventlog is a very simple Event logger you can use to track certain
events in your code. I use it primarily in background task queues to keep
track if tasks executed properly.

django-eventlog stores it's data in a regular database model, so each log entry
will trigger a SQL Insert. Therefore you should be careful using it in high
performance and/or high volume tasks.

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

A new Event is started by the ``Event`` object. It has two required
arguments: The type and a text message. django-eventlog comes with a almost
hand full of pre-defined type choices (but you can extend it, see below):

- ``EventChoices.started``
- ``EventChoices.in_progress``
- ``EventChoices.done``
- ``EventChoices.single`` (Default type if none is provided)

See this example where I create two event entries in an arbitrary task
function:

.. code-block:: python

    from eventlog.events import Event, EventChoices as E

    @BackgroundTask()
    def long_running_task(request):

        # Start a new Event.
        e = Event(E.started, message='Sending 100000 emails to all users.',
                  initiator=request.user.email)

        # ... sending 100000 totally not spam emails...

        # Attach further events using the log function.
        e.log(E.done, message='All emails sent!', initiator=request.user.email)


Each event will show up in the Django Admin changelog view. If you hover over
one, it will highlight all related events as well.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png
   :scale: 100 %

A bit less verbose
------------------

.. code-block:: python

    # You can also pass the type as a string if you prefer it.
    # This is the same as above.
    e.log('done', message='All emails sent!', initiator=request.user.email)

    # You can also leave the type away, then the default type ``single``
    # is used.
    e.log(message='Just wanted to say hi!')

Email notification
------------------

You can notify yourself via email by adding the ``send_email`` argument
to a log call.

.. code-block:: python

    e.log(E.done, 'Conquered the world!', initiator='The cat',
          send_email='the-cat@example.com')

``@eventlog`` decorator
-----------------------

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
    from eventlog.apps import EventLogConfig

    class CustomEventLogConfig(EventLogConfig):
        def event_type_choices(self):
            """
            List of event types to be used in events.
            """
            from model_utils import Choices
            return Choices(
                (1, 'started', 'Started'),
                (2, 'working', 'Working on it'),
                (3, 'still', 'Still working on it'),
                (4, 'yay', 'Yay!'),
                (5, 'single', 'One Time Event'),
            )

        @property
        def default_event_type(self):
            """
            The default event type if not provided in an event log.
            """
            return 5  # single


    # settings.py
    INSTALLED_APPS = [
        # Use your custom Config instead of ``eventlog.apps.EventLogConfig``
        'myproject.CustomEventLogConfig',
    ]


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
