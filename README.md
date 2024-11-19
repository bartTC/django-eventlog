[![](https://img.shields.io/pypi/v/django-eventlog.svg)](https://pypi.org/project/django-eventlog/)
[![](https://github.com/bartTC/django-eventlog/actions/workflows/push.yml/badge.svg)](https://github.com/bartTC/django-eventlog/actions/workflows/push.yml)
[![](https://codecov.io/github/bartTC/django-eventlog/graph/badge.svg?token=YLXXbCawUQ)](https://codecov.io/github/bartTC/django-eventlog)

---

📖 **Full documentation: https://barttc.github.io/django-eventlog/**

_Compatibility Matrix:_

| Py/Dj     | 3.9 | 3.10 | 3.11 | 3.12 | 3.13 |
| --------- | --- | ---- | ---- | ---- |------|
| 4.2 (LTS) | ✓   | ✓    | ✓    | ✓    | ✓    |
| 5.0       | —   | ✓    | ✓    | ✓    | ✓    |
| 5.1       | —   | ✓    | ✓    | ✓    | ✓    |

# django-eventlog

<img src="https://github.com/bartTC/django-eventlog/raw/main/docs/_static/logo.webp" alt="djang-eventlog Logo" width="300"/>

django-eventlog is a very simple event logger you can use to track certain actions in
your code. Events are stored in a Django model and can be viewed in the Django Admin.

Usage Example:

```python
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
```

You can reuse an event group by specifying a group name and attach optional data. Data
must be JSON serializable.

```python
from eventlog import EventGroup

def purchase():
    e = EventGroup(group_id=f"Order {self.order.pk}")
    e.info("Sent order to Shopify", data={"items": [1, 2, 3]})

def subscribe_newsletter():
    e = EventGroup(group_id=f"Order {self.order.pk}")
    e.info("User subscribed to newsletter on checkout", data={"email": "user@example.com"})
```

Events can be grouped in a "Event Group" and when hovering over one item in the admin,
all events of the same group are highlighted:

![](https://github.com/bartTC/django-eventlog/raw/main/docs/_static/change_list.png)

The details view of an event will list all other events of this group so you
can track the progress:

![](https://github.com/bartTC/django-eventlog/raw/main/docs/_static/change_form.png)

While looking similar, it's not intended to be a replacement for your regular Python
`logging` facility, rather an addition to it.

django-eventlog stores it's data in a regular database model, so each log entry will
trigger a SQL Insert. Therefore you should be careful using it in high performance
and/or high volume environments.
