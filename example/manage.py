#!/usr/bin/env python
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
    # Same effect as python -Wd when run via coverage:
    import warnings

    warnings.simplefilter("always", DeprecationWarning)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    # Allow starting the app without installing the module.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    execute_from_command_line(sys.argv)
