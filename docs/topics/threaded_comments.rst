Adding threaded comments
========================

This package has build-in support for django-threadedcomments_ in this module.
It can be enabled using the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'threadedcomments',
    )

    COMMENTS_APP = 'fluent_comments'

And make sure the intermediate ``ThreadedComment`` model is available and filled with data::

    ./manage.py migrate
    ./manage.py migrate_comments

The templates and admin interface adapt themselves automatically
to show the threaded comments.

.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments
