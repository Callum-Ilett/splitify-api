#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    from django.conf import settings

    if os.environ.get("RUN_MAIN") and settings.DEBUG:
        import debugpy  # noqa: T100

        debugpy.listen(("0.0.0.0", 3000))  # noqa: S104, T100

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        error_message = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(error_message) from None
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
