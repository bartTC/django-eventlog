from pathlib import Path

DEBUG = True

TESTAPP_DIR = Path(__file__).resolve().parent

SECRET_KEY = "testsecretkey"  # noqa: S105 hardcoded password

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": TESTAPP_DIR / "testdb.sqlite",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_ROOT = TESTAPP_DIR / ".static"
MEDIA_ROOT = TESTAPP_DIR / ".uploads"

STATIC_URL = "/static/"
MEDIA_URL = "/uploads/"

ROOT_URLCONF = "eventlog.tests.testapp.urls"

INSTALLED_APPS = [
    "eventlog.apps.EventLogConfig",
    "eventlog.tests.testapp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
