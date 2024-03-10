# Installation and Usage

## Installation:

Install django-eventlog via pip:

```bash
$ pip install django-eventlog
```

Then add ``eventlog.apps.EventLogConfig`` to your ``INSTALLED_APPS``
setting and migrate the database as usual.

```python
INSTALLED_APPS = [
    # ...
    'eventlog.apps.EventLogConfig',
]
```

## Usage

A new Event group is started by the ``EventGroup`` object, which you can call
with individual "types" similar to logging levels in Python logging.

```python
from eventlog import EventGroup
from itertools import batched

emails = [...]

# Start a new Event group
e = EventGroup()
e.info('Starting to send 100,000 emails.', initiator='Mailer Daemon')

try: 
    for batch in batched(emails, 1_000):
        # ... send 1000 emails per batch
        e.info(f"{batch} emails sent...", initiator='Mailer Daemon')
except RuntimeError:
    e.error("Mail server unexpectedly quit!", initiator='Mailer Daemon')
    
# All mails sent successfully.
e.info('All emails sent!', initiator='Mail Sender')
```

This example will store two ``info`` events. Each event will show up in the
Django Admin changelog view. If you hover over one, it will highlight all
related events as well.

![](https://github.com/bartTC/django-eventlog/raw/main/docs/_static/change_form.png)

Event types are pre-defined in django-eventlog, but you can define your own
(see [Custom Event Types](settings.md)). You can use them to distinct your events and also filter them in
the admin view later. For example to only see `error` events.
Currently these event types are defined:

- `info`
- `warning`
- `error`
- `critical`

### Re-use event groups

You can re-use the same event group through the code, if you pass a fixed group name:

```python
from eventlog import EventGroup

# fileA.py
e = EventGroup(group_id="abc")
e.info('This is a message')

# fileB.py
e = EventGroup(group_id="abc")
e.info('This is another message attached to the same group')
```

## Email Notification

You can notify yourself via email by adding the `send_mail` argument to a log call.

```python
from eventlog import EventGroup

e = EventGroup()
e.info('This event sends an email.',  send_mail='user@example.com')
e.info('This one too.',  send_mail='user@example.com')
e.info('This one does not.')
```

You can also pass `send_mail` to the `EventGroup` class. This way it's globally enabled 
for all events of this group. In this example, three emails are sent.

```python
from eventlog import EventGroup

e = EventGroup(send_mail='user@example.com')
e.info('This will send one email.')
e.info('This will send one email as well.')
e.info('This will send one email also.')
```
