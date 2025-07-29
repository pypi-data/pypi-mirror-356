#!/usr/bin/env python
import django
from django.conf import settings


settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "htpayway",
    ],
    MIDDLEWARE_CLASSES=[],
)
django.setup()


if __name__ == "__main__":
    from django.test.utils import get_runner

    test_runner = get_runner(settings)()
    result = test_runner.run_tests(["htpayway"])
