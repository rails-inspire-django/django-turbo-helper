import os
import pathlib

import pytest


def pytest_configure():
    from django.conf import settings

    settings.configure(
        SECRET_KEY="seekret",
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "mem_db"},
        },
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [pathlib.Path(__file__).parent.absolute() / "templates"],
                "APP_DIRS": True,
                "OPTIONS": {
                    "debug": False,
                    "context_processors": [],
                    "builtins": [],
                    "libraries": {},
                },
            }
        ],
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "turbo_helper",
            "channels",
            "tests.testapp.apps.TestAppConfig",
        ],
        ROOT_URLCONF="tests.testapp.urls",
        CHANNEL_LAYERS={
            "default": {
                "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
                "CONFIG": {
                    "hosts": [os.getenv("CHANNEL_LAYERS", "redis://localhost:6379/0")],
                },
            },
        },
    )


@pytest.fixture
def todo():
    from tests.testapp.models import TodoItem

    return TodoItem.objects.create(description="test")
