.. _testing:

=============================
Testing and Local Development
=============================

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

