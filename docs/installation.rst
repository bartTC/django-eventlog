.. _installation:

============
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
`Custom Event Types`_.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'eventlog',
    ]
