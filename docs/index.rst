.. _index:

===============
django-eventlog
===============


.. toctree::
   :maxdepth: 1

   installation
   usage
   settings
   testing


django-eventlog is a very simple Event logger you can use to track certain
events in your code. Events are stored in a Django model and can be viewed
in the Django Admin.

Events can be grouped in a "Event Group" and when hovering over one item
in the admin, all events of the same group are highlighted.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png

While looking similar, it's not intended to be a replacement for your regular
Python ``logging`` facility, rather an addition to it.

My intention was that users with no access to regular log files can see the
progress and success of certain events. I use it primarily in Task Queues
like Celery_ to inform staff user about the state of background tasks.

django-eventlog stores it's data in a regular database model, so each log entry
will trigger a SQL Insert. Therefore you should be careful using it in high
performance and/or high volume environments.

.. _Celery: http://www.celeryproject.org/
