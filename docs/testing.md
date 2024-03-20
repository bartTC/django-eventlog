# Testing and Local Development

The project is using [Poetry](https://python-poetry.org) to manage the local configuation. Install it with:

```bash
$ pip install poetry
```

Then install the project dependencies:

```bash
$ cd django-eventlog/
$ poetry install
```

Run the testsuite in your local environment using::=
    
```bash
$ poetry run tests
```

Or use tox to test against various Django and Python versions:

```bash
$ tox run-parallel --recreate
```

You can also invoke the test suite or other 'manage.py' commands by calling the 
`django-admin` tool with the test app settings:

```bash
$ export DJANGO_SETTINGS_MODULE=eventlog.tests.testapp.settings
$ poetry run django-admin
$ poetry run django-admin makemigrations --dry-run
```

You can also run the `runserver` and use the `testapp` for visual testing:

```bash
$ poetry run django-admin runserver
```

## Build this documentation

This is also done via Poetry:

```bash
$ poetry run mkdocs build  # Build docs
$ poetry run mkdocs serve  # Serve a development server with live reloads
```
