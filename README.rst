.. image:: https://img.shields.io/pypi/v/django-eventlog.svg
    :target: https://pypi.org/project/django-eventlog/

.. image:: https://github.com/bartTC/django-eventlog/actions/workflows/push.yml/badge.svg
    :target: https://github.com/bartTC/django-eventlog/actions/workflows/push.yml

-----

📖 **Full documentation: https://django-eventlog.readthedocs.io/**

*Compatibility Matrix:*

========= === === ==== ==== ====
Py/Dj     3.8 3.9 3.10 3.11 3.12
========= === === ==== ==== ====
3.2 (LTS)  ✓   ✓   ✓    ✓    ✓
4.0        ✓   ✓   ✓    ✓    ✓
4.1        ✓   ✓   ✓    ✓    ✓
4.2 (LTS)  ✓   ✓   ✓    ✓    ✓
5.0        —   —   ✓    ✓    ✓
========= === === ==== ==== ====

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

.. image:: https://github.com/bartTC/django-eventlog/raw/main/docs/_static/change_list.png
   :scale: 100 %

The details view of an event will list all other events of this group so you
can track the progress:

.. image:: https://github.com/bartTC/django-eventlog/raw/main/docs/_static/change_form.png
   :scale: 100 %

.. note::

  While looking similar, it's not intended to be a replacement for your
  regular Python ``logging`` facility, rather an addition to it.

  django-eventlog stores it's data in a regular database model, so each log entry
  will trigger a SQL Insert. Therefore you should be careful using it in high
  performance and/or high volume environments.
