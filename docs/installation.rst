.. _installation:

======================
Installation and Usage
======================

Installation:
=============

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
`Custom Event Types`_.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'eventlog',
    ]

.. _usage:

Usage
=====

A new Event group is started by the ``EventGroup`` object, which you can call
with individual "types" similar to logging levels in Python logging.

.. code-block:: python

    from eventlog.events import EventGroup

    # Start a new Event group
    e = EventGroup()
    e.info('Starting to send 100000 emails to all users.', initiator='Mail Sender')
    # ... sending 100000 totally not spam emails...
    e.info('All emails sent!', initiator='Mail Sender')

This example will store two ``info`` events. Each event will show up in the
Django Admin changelog view. If you hover over one, it will highlight all
related events as well.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png
   :scale: 100 %

Event types are pre-defined in django-eventlog, but you can define your own
(see `Custom Event Types`_). You can use them to distinct your events and also filter them in
the admin view later. For example to only see ``error`` events.
Currently these event types are defined:

- ``info``
- ``warning``
- ``error``
- ``critical``


Email Notification
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

