Configuration reference
=======================

The default settings are:

.. code-block:: python

    AKISMET_API_KEY = None
    AKISMET_BLOG_URL = None
    AKISMET_IS_TEST = False

    CRISPY_TEMPLATE_PACK = 'bootstrap'

    FLUENT_COMMENTS_REPLACE_ADMIN = True

    # Akismet spam fighting
    FLUENT_CONTENTS_USE_AKISMET = bool(AKISMET_API_KEY)
    FLUENT_COMMENTS_AKISMET_ACTION = 'soft_delete'

    # Moderation
    FLUENT_COMMENTS_DEFAULT_MODERATOR = 'default'
    FLUENT_COMMENTS_CLOSE_AFTER_DAYS = None
    FLUENT_COMMENTS_MODERATE_BAD_WORDS = ()
    FLUENT_COMMENTS_MODERATE_AFTER_DAYS = None
    FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = True

    # Form layouts
    FLUENT_COMMENTS_FIELD_ORDER = ()
    FLUENT_COMMENTS_EXCLUDE_FIELDS = ()
    FLUENT_COMMENTS_FORM_CLASS = None
    FLUENT_COMMENTS_FORM_CSS_CLASS = 'comments-form form-horizontal'
    FLUENT_COMMENTS_LABEL_CSS_CLASS = 'col-sm-2'
    FLUENT_COMMENTS_FIELD_CSS_CLASS = 'col-sm-10'

    # Compact style settings
    FLUENT_COMMENTS_COMPACT_FIELDS = ('name', 'email', 'url')
    FLUENT_COMMENTS_COMPACT_GRID_SIZE = 12
    FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS = "col-sm-{size}"


.. _FLUENT_COMMENTS_FORM_CLASS:

FLUENT_COMMENTS_FORM_CLASS
--------------------------

Defines a dotted Python path to the form class to use.
The built-in options include:

Standard forms:

* ``fluent_comments.forms.DefaultCommentForm`` The standard form.
* ``fluent_comments.forms.CompactLabelsCommentForm`` A form where labels are hidden.
* ``fluent_comments.forms.CompactCommentForm`` A compact row

Variations with reCAPTCHA v2:

* ``fluent_comments.forms.recaptcha.DefaultCommentForm``
* ``fluent_comments.forms.recaptcha.CompactLabelsCommentForm``
* ``fluent_comments.forms.recaptcha.CompactCommentForm``

Variations wiwth a simple self-hosted captcha:

* ``fluent_comments.forms.captcha.DefaultCommentForm``
* ``fluent_comments.forms.captcha.CompactLabelsCommentForm``
* ``fluent_comments.forms.captcha.CompactCommentForm``


.. _FLUENT_COMMENTS_AKISMET_ACTION:

FLUENT_COMMENTS_AKISMET_ACTION
------------------------------

What to do when spam is detected, see :ref:`akismet_usage`.


.. _FLUENT_COMMENTS_FIELD_ORDER:

FLUENT_COMMENTS_FIELD_ORDER
---------------------------

Defines the field ordering, see :ref:`field-order`.
