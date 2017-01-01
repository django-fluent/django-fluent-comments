#!/bin/sh

python -c "
import sys, django, os
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5], sys.executable))
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(), os.path.dirname(os.path.abspath(django.__file__))))
"

exec example/manage.py test "$@"
