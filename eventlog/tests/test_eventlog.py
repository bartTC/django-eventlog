from datetime import timedelta
from http import HTTPStatus
from typing import Any

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains

from eventlog.admin import get_difference
from eventlog.datastructures import EventType
from eventlog.events import EventGroup
from eventlog.models import Event


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
def test_multiuse_named_log() -> None:
    """Multiple log items, initialized twice with the same group id."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup(group_id="abc")
    e.info("Hello World")
    e.error("Hello World")

    e = EventGroup(group_id="abc")
    e.warning("Hello World")
    e.critical("Hello World")

    assert Event.objects.count() == 4
    assert Event.objects.filter(group="abc").count() == 4


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
def test_mail_per_event(mailoutbox: Any) -> None:
    """Send one mail per event."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup()
    e.info("Hello World", send_mail="user@example.com")
    e.error("Hello World")
    e.warning("Hello World")
    e.critical("Hello World", send_mail="user@example.com")
    assert Event.objects.count() == 4
    assert len(mailoutbox) == 2


@pytest.mark.django_db()
def test_mail_per_group(mailoutbox: Any) -> None:
    """Set mail per group so it's sent for every event."""
    from eventlog import EventGroup
    from eventlog.models import Event

    e = EventGroup(send_mail="user@example.com")
    e.info("Hello World")
    e.error("Hello World")
    e.warning("Hello World")
    e.critical("Hello World")
    assert Event.objects.count() == 4
    assert len(mailoutbox) == 4


@pytest.mark.django_db()
def test_admin_changelist(admin_client: Client) -> None:
    """
    Admin Changelist will render all events and legacy events
    They exist in db but no longer defined in AppConfig.
    """

    # Regular Event
    e = EventGroup(group_id="abc")
    e.info("Hello World 1")
    e.info("Hello World 2")
    e.error("Hello World 3")
    e.warning("Hello World 4")

    # Legacy Event (Created and in database, but its type no longer valid)
    Event.objects.create(
        type="legacy_event",
        group="abc",
        message="This is some info.",
    )

    changelist_url = reverse("admin:eventlog_event_changelist")
    response = admin_client.get(changelist_url)

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Hello World 1")
    assertContains(response, "Hello World 2")
    assertContains(response, "Hello World 3")
    assertContains(response, "Hello World 4")
    assertContains(response, "Legacy_Event")


@pytest.mark.django_db()
def test_admin_changeform(admin_client: Client) -> None:
    """Admin Changeform is OK."""

    e1 = EventGroup()
    e1.info("Hello World 1")
    e1.info("Hello World 2")

    # Legacy Event — created and in database, but its type no longer valid. Create a
    # couple of them to test different 'day/hour/minute' delays between events.
    Event.objects.create(
        type="legacy_event",
        group=e1.group_id,
        message="This is some info.",
        timestamp=timezone.now() + timedelta(minutes=2),
    )

    # A second group, which is not rendered on the change form.
    e2 = EventGroup()
    e2.error("Hello World 3")
    e2.warning("Hello World 4")

    obj = Event.objects.filter(group=e1.group_id).first()
    changeform_url = reverse("admin:eventlog_event_change", args=(obj.pk,))
    response = admin_client.get(changeform_url)

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Hello World 1")
    assertContains(response, "Hello World 2")
    assertContains(response, "Legacy_Event")

    # These are a different group
    assertNotContains(response, "Hello World 3")
    assertNotContains(response, "Hello World 4")


@pytest.mark.django_db()
def test_admin_changeform_delays(admin_client: Client) -> None:
    """
    Create a list of events, all minutes/days/years apart,
    to make sure; the various 'delay' timestamps don't break.
    """
    now = timezone.now()
    e = EventGroup()
    e1 = Event.objects.create(group=e.group_id, type="info", message="A")
    e2 = Event.objects.create(group=e.group_id, type="info", message="B")
    e3 = Event.objects.create(group=e.group_id, type="info", message="C")
    e4 = Event.objects.create(group=e.group_id, type="info", message="D")
    e5 = Event.objects.create(group=e.group_id, type="info", message="E")
    e6 = Event.objects.create(group=e.group_id, type="info", message="F")

    # Because "timestamp" is an auto_now field, we can't set it directly
    # but have to do this detour.
    Event.objects.filter(pk=e1.pk).update(timestamp=now)
    Event.objects.filter(pk=e2.pk).update(timestamp=now + timedelta(seconds=1))
    Event.objects.filter(pk=e3.pk).update(timestamp=now + timedelta(hours=1))
    Event.objects.filter(pk=e4.pk).update(timestamp=now + timedelta(days=1))
    Event.objects.filter(pk=e5.pk).update(timestamp=now + timedelta(weeks=1))
    Event.objects.filter(pk=e6.pk).update(timestamp=now + timedelta(weeks=52))

    obj = Event.objects.filter(group=e.group_id).first()
    changeform_url = reverse("admin:eventlog_event_change", args=(obj.pk,))
    response = admin_client.get(changeform_url)

    assert response.status_code == HTTPStatus.OK


def test_invalid_type_usage() -> None:
    """Calling an invalid type will raise an error."""
    e = EventGroup()

    with pytest.raises(TypeError):
        e.doesnotexist("Hello World")


def test_invalid_type_creation() -> None:
    """Creating an invalid type will raise an error."""
    with pytest.raises(TypeError):
        EventType(
            name="1invalid_name",
            label="Must not start with number",
        )


def test_group_name_too_long() -> None:
    """Group ids are limited to 40 characters."""
    EventGroup(group_id="a" * 40)

    with pytest.raises(TypeError):
        EventGroup(group_id="a" * 41)


def test_type_name_too_long() -> None:
    """Type names (.info, .warning) are limited to 50 characters."""
    EventType(name="a" * 50, label="50 chars is OK")

    with pytest.raises(TypeError):
        EventType(name="a" * 51, label="Must not exceed 50 characters")


def test_duration() -> None:
    """Test duration string calcuated for the time between two Events."""
    now = timezone.now()

    diff = get_difference(Event(timestamp=now), Event(timestamp=now))
    assert diff == "- same time"

    diff = get_difference(
        Event(timestamp=now), Event(timestamp=now + timedelta(seconds=10))
    )
    assert diff == "10s later"

    diff = get_difference(
        Event(timestamp=now), Event(timestamp=now + timedelta(seconds=10, minutes=5))
    )
    assert diff == "5m 10s later"

    diff = get_difference(
        Event(timestamp=now),
        Event(timestamp=now + timedelta(seconds=10, minutes=5, hours=2)),
    )
    assert diff == "2h 5m 10s later"

    diff = get_difference(
        Event(timestamp=now),
        Event(timestamp=now + timedelta(seconds=10, minutes=5, hours=2, days=3)),
    )
    assert diff == "3d 2h 5m 10s later"

    diff = get_difference(
        Event(timestamp=now),
        Event(timestamp=now + timedelta(seconds=10, minutes=5, hours=2, days=400)),
    )
    assert diff == "1y 35d 2h 5m 10s later"
