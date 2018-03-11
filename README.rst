.. image:: https://travis-ci.org/bartTC/django-eventlog.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-eventlog

.. image:: https://codecov.io/github/bartTC/django-eventlog/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-eventlog?branch=master

Full documentation: https://docs.elephant.house/django-eventlog/

===============
django-eventlog
===============

django-eventlog is a very simple event logger you can use to track certain
actions in your code. Events are stored in a Django model and can be viewed
in the Django Admin.

Usage Example::

    from eventlog import EventGroup

    e = EventGroup()                       # Start a new Event Group
    e.info('About to send 1000 mails.',    # Trigger an Event
           initiator='Mailer Daemon')
    try:
        # ... sending 1000 mails
        e.info('All emails sent!',         # Trigger an Event in the same group,
               initiator='Mailer Daemon')  # so they are combined in the admin.
    except Exception:
        e.error('There was an error sending the emails.',
                initiator='Mailer Daemon')


Events can be grouped in a "Event Group" and when hovering over one item
in the admin, all events of the same group are highlighted:

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/change_list.png
   :scale: 100 %

The details view of an event will list all other events of this group so you
can track the progress:

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/change_form.png
   :scale: 100 %

.. note::

  While looking similar, it's not intended to be a replacement for your
  regular Python ``logging`` facility, rather an addition to it.

  django-eventlog stores it's data in a regular database model, so each log entry
  will trigger a SQL Insert. Therefore you should be careful using it in high
  performance and/or high volume environments.
