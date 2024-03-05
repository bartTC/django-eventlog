from io import StringIO

import pytest
from django.core.management import call_command


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
