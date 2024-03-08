from http import HTTPStatus
from uuid import uuid4

import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains


@pytest.mark.django_db()
def test_simple_log() -> None:
    """Simple log item."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World")
    assert Event.objects.count() == 1


@pytest.mark.django_db()
def test_multi_log() -> None:
    """Multiple log items."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World")
    e.error("Hello World")
    e.warning("Hello World")
    e.critical("Hello World")
    assert Event.objects.count() == 4


@pytest.mark.django_db()
def test_data_log() -> None:
    """Simple log item with data."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World", data={"email": "user@example.com"})
    e.info("Hello World", data={"foo": {"bar": [1, 2, 3]}})
    assert Event.objects.count() == 2


@pytest.mark.django_db()
def test_unserializable_data_log() -> None:
    """Log item with data that's not JSON serializable."""
    from eventlog import EventGroup
    from eventlog.models import Event

    class Foo:
        pass

    e = EventGroup()
    e.info("Hello World", data={"foo": Foo()})
    assert Event.objects.count() == 1

    # It will be barely readable but better than failing upon a log entry.
    assert "Foo object" in Event.objects.first().data


@pytest.mark.django_db()
def test_invalid_type() -> None:
    """Calling an invalid type will raise an error."""
    from eventlog import EventGroup

    e = EventGroup()
    with pytest.raises(AttributeError):
        e.doesnotexist("Hello World")


@pytest.mark.django_db()
def test_mail_per_event() -> None:
    """Send one mail per event."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World", send_mail="user@example.com")
    e.error("Hello World")
    e.warning("Hello World")
    e.critical("Hello World", send_mail="user@example.com")
    assert Event.objects.count() == 4
    assert len(mail.outbox) == 2


@pytest.mark.django_db()
def test_mail_per_group() -> None:
    """Send one mail per event."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup(send_mail="user@example.com")
    e.info("Hello World")
    e.error("Hello World")
    e.warning("Hello World")
    e.critical("Hello World")  # Explicitly disabled
    assert Event.objects.count() == 4
    assert len(mail.outbox) == 4


@pytest.mark.django_db()
def test_admin_changelist(client: Client) -> None:
    """Admin Changelist is OK."""
    from django.contrib.auth.models import User

    from eventlog import EventGroup
    from eventlog.models import Event

    # Regular Event
    e = EventGroup()
    e.info("Hello World")
    e.info("Hello World 2")
    e.error("Hello World 3")
    e.warning("Hello World 4")

    # Legacy Event (Created and in database, but its type no longer valid)
    Event.objects.create(
        type="Legacy Event",
        group=uuid4().hex,
        message="This is some info.",
        initiator="Test Runner",
    )

    User.objects.create_superuser("jon", "jon@example.com", "foobar")
    client.login(
        username="jon",
        password="foobar",  # noqa: S106 Hardcoded password
    )

    changelist_url = reverse("admin:{}_{}_changelist".format("eventlog", "event"))
    response = client.get(changelist_url)

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Hello World")


@pytest.mark.django_db()
def test_admin_changeform(client: Client) -> None:
    """Admin Changeform is OK."""
    from django.contrib.auth.models import User

    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World")
    e.info("Hello World 2")
    e.error("Hello World 3")
    e.warning("Hello World 4")

    obj = Event.objects.first()
    User.objects.create_superuser("jon", "jon@example.com", "foobar")
    client.login(
        username="jon",
        password="foobar",  # noqa: S106 Hardcoded password
    )

    changelist_url = reverse(
        "admin:{}_{}_change".format("eventlog", "event"),
        args=(obj.pk,),
    )
    response = client.get(changelist_url)

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Hello World")
