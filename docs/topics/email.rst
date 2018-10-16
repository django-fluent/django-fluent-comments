E-mail notification
===================

By default, the ``MANAGERS`` of a Django site will receive an e-mail notification of new comments.
This feature can be enabled or disabled using:

.. code-block:: python

    FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = False

By default, plain-text e-mail messages are generated using the template ``comments/comment_notification_email.txt``.

Multi-part (HTML) e-mails are supported using the template ``comments/comment_notification_email.html``. To enabled
multi-part e-mails, set:

.. code-block:: python

    FLUENT_COMMENTS_MULTIPART_EMAILS = True

In addition to the standard django-comments_ package, the ``request`` and ``site`` fields
are available in the template context data. This allows generating absolute URLs to the site.

.. _django-comments: https://github.com/django/django-contrib-comments
