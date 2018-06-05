Auto comment moderation
=======================

By default, any comment receives moderation from the "default moderator"
This ensures random comments also receive :doc:`akismet <akismet>` checks,
bad word filtering and send :doc:`email notifications <email>`.

Some moderation features require more knowledge of the model.
This includes:

* Toggling an "enable comments" checkbox on the model.
* Auto-closing comments after X days since the publication of the article.
* Auto-moderating comments after X days since the publication of the article.

Comment moderation can be enabled for the specific models using:

.. code-block:: python

    from fluent_comments.moderation import moderate_model
    from myblog.models import BlogPost

    moderate_model(BlogPost,
        publication_date_field='publication_date',
        enable_comments_field='enable_comments',
    )

This code can be placed in a ``models.py`` file.
The provided field names are optional. By providing the field names,
the comments can be auto-moderated or auto-closed after a number of days since the publication date.

The following settings are available for comment moderation:

.. code-block:: python

    FLUENT_COMMENTS_CLOSE_AFTER_DAYS = None         # Auto-close comments after N days
    FLUENT_COMMENTS_MODERATE_AFTER_DAYS = None      # Auto-moderate comments after N days.

The default moderator
---------------------

The default moderator is configurable using:

.. code-block:: python

    FLUENT_COMMENTS_DEFAULT_MODERATOR = 'default'

Possible values are:

* ``default`` installs the standard moderator that all packages use.
* ``deny`` will reject all comments placed on models which don't have an explicit moderator registered with ``moderate_model()``.
* ``None`` will accept all comments, as if there is no default moderator installed.
* A dotted Python path will import this class.

When using a custom moderator class, consider inheriting
``fluent_comments.moderation.FluentCommentsModerator``
to preserve the email notification feature.
