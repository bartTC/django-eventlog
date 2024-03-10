# Testing and Local Development

The project is using [pipenv]() to manage the local configuation. Install it with:

```bash
$ cd django-eventlog/

$ pip install pipenv
$ pipenv install --dev
```

Run the testsuite in your local environment using::=
    
```bash
$ pipenv run test
```

Or use tox to test against various Django and Python versions:

```bash
$ tox -r
```


You can also invoke the test suite or other 'manage.py' commands by calling the 
`django-admin` tool with the test app settings:

```bash
$ pipenv run django-admin
$ pipenv run django-admin test
$ pipenv run django-admin makemigrations --dry-run
```

You can also run the `runserver` and use the `testapp` for visual testing:

```bash
$ pipenv run django-admin runserver
```