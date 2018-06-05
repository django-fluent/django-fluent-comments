E-mail notification
===================

By default, the ``MANAGERS`` of a Django site will receive an e-mail notification of new comments.
This feature can be enabled or disabled using:

.. code-block:: python

    FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = False

The template ``comments/comment_notification_email.txt`` is used to generate the e-mail message.

In addition to the standard django-comments_ package, the ``request`` and ``site`` fields
are available in the template context data. This allows generating absolute URLs to the site.

.. _django-comments: https://github.com/django/django-contrib-comments
