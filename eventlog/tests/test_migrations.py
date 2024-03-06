from io import StringIO

import pytest
from django.core.management import call_command
from pytest_django.fixtures import SettingsWrapper


@pytest.mark.django_db()
def test_no_pending_migrations() -> None:
    """
    Ensure there aer no pending migrations.
    """
    app_name = "eventlog"

    out = StringIO()
    call_command(
        "makemigrations",
        app_name,
        dry_run=True,
        verbosity=1,
        interactive=False,
        stdout=out,
        stderr=out,
    )

    out.seek(0)
    response = out.getvalue()

    if f"No changes detected in app '{app_name}'" not in response:
        pytest.fail(
            f"Pending migrations in app {app_name}. "
            f"Run `manage.py makemigrations {app_name}.` "
            f"\n\n{response}",
        )


@pytest.mark.django_db()
def test_no_pending_migrations_if_autofield_differs(settings: SettingsWrapper) -> None:
    """
    If the base settings use a different autofield than the app,
    it must not trigger a migration.
    """
    settings.DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    test_no_pending_migrations()
