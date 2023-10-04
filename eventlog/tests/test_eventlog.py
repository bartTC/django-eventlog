from uuid import uuid4

from django.core import mail
from django.test import TestCase
from django.urls import reverse


class EventLogTestCase(TestCase):
    def test_simple_log(self) -> None:
        """Simple log item."""
        from eventlog import EventGroup
        from eventlog.models import Event

        e = EventGroup()
        e.info("Hello World")
        assert Event.objects.count() == 1

    def test_multi_log(self) -> None:
        """Multiple log items."""
        from eventlog import EventGroup
        from eventlog.models import Event

        e = EventGroup()
        e.info("Hello World")
        e.error("Hello World")
        e.warning("Hello World")
        e.critical("Hello World")
        assert Event.objects.count() == 4

    def test_invalid_type(self) -> None:
        """Calling an invalid type will raise an error."""
        from eventlog import EventGroup

        e = EventGroup()
        with self.assertRaises(AttributeError):
            e.doesnotexist("Hello World")

    def test_mail_per_event(self) -> None:
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

    def test_mail_per_group(self) -> None:
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

    def test_admin_changelist(self) -> None:
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
        self.client.login(
            username="jon",
            password="foobar",  # noqa: S106 Hardcoded password
        )

        changelist_url = reverse("admin:{}_{}_changelist".format("eventlog", "event"))
        response = self.client.get(changelist_url)

        assert response.status_code == 200
        self.assertContains(response, "Hello World")

    def test_admin_changeform(self) -> None:
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
        self.client.login(
            username="jon",
            password="foobar",  # noqa: S106 Hardcoded password
        )

        changelist_url = reverse(
            "admin:{}_{}_change".format("eventlog", "event"),
            args=(obj.pk,),
        )
        response = self.client.get(changelist_url)

        assert response.status_code == 200
        self.assertContains(response, "Hello World")
