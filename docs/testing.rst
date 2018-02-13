.. _testing:

=============================
Testing and Local Development
=============================

Run the testsuite in your local environment using::

    $ cd django-eventlog/
    $ pipenv intall --dev
    $ pipenv run django-admin test

Or use tox to test against various Django and Python versions::

    $ tox -r


You can also invoke the test suite or other 'manage.py' commands by calling
the ``django-admin`` tool with the test app settings::

    $ cd django-eventlog/
    $ pipenv install --dev
    $ pipenv run django-admin
    $ pipenv run django-admin test
    $ pipenv run django-admin makemigrations --dry-run

You can also run the ``runserver`` and use the ``testapp`` for visual testing::

    $ pipenv run django-admin runserver
