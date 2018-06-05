.. _akismet_usage:

Akismet spam detection
======================

Akismet_ is used out of the box when the ``AKISMET_API_KEY`` setting is defined:

.. code-block:: python

    AKISMET_API_KEY = "your-api-key"

This can also be enabled explicitly:

.. code-block:: python

    FLUENT_CONTENTS_USE_AKISMET = True  # Enabled by default when AKISMET_API_KEY is set.

The following settings are optional:

.. code-block:: python

    AKISMET_BLOG_URL = "http://example.com"  # Optional, to override auto detection
    AKISMET_IS_TEST = False  # Enable to make test runs

When spam is detected, the default behavior depends on the spam score.
Obvious spam is discarded with an HTTP 400 response, while possible spam is marked for moderation.

The :ref:`FLUENT_COMMENTS_AKISMET_ACTION` setting can be one of these values:

* ``auto`` chooses between ``moderate``, ``soft_delete`` and ``delete`` based on the spam score.
* ``moderate`` will always mark the comment for moderation.
* ``soft_delete`` will mark the comment as moderated + removed, but it can still be seen in the admin.
* ``delete`` will outright reject posting the comment and respond with a HTTP 400 Bad Request.

.. tip::

    By default, Akismet will not report any post from the Django superuser as spam.
    Comments with the name "viagra-test-123" will always be flagged as spam.

.. warning::

    Akismet is a third party service by Automattic.
    Note that :doc:`GDPR Compliance <gdpr>` is next-to-impossible with this service.

.. _Akismet: http://akismet.com
