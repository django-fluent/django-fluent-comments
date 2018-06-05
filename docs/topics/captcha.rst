Captcha support
===============

Users can be required to enter a captcha.

This is done by changing the :ref:`FLUENT_COMMENTS_FORM_CLASS` setting.

.. note::

    When :ref:`FLUENT_COMMENTS_FIELD_ORDER` is configured, also include the ``"captcha"`` field!

Using django-recaptcha
----------------------

django-recaptcha_ provides "no captcha" reCAPTCHA v2 support.
Choose one of the form layout classes:

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.DefaultCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.CompactLabelsCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.CompactCommentForm'

And configure it's settings:

.. code-block:: python

    RECAPTCHA_PUBLIC_KEY = "the Google provided site_key"
    RECAPTCHA_PRIVATE_KEY = "the Google provided secret_key"

    NOCAPTCHA = True  # Important! Required to get "no captcha reCAPTCHA v2

    INSTALLED_APPS += (
        'captcha',
    )

Using django-nocaptcha-recaptcha
---------------------------------

django-nocaptcha-recaptcha_ also provides "no captcha" reCAPTCHA v2 support.
The same form classes are used, as the correct imports are detected at startup:

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.DefaultCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.CompactLabelsCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.recaptcha.CompactCommentForm'

It's settings differ slightly:

.. code-block:: python

    NORECAPTCHA_SITE_KEY = "the Google provided site_key"
    NORECAPTCHA_SECRET_KEY = "the Google provided secret_key"

    INSTALLED_APPS += (
        'nocaptcha_recaptcha',
    )

Using django-simple-captcha
---------------------------

django-simple-captcha_ provides a simple local captcha test.
It does not require external services, but it can be easier to break.

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.captcha.DefaultCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.captcha.CompactLabelsCommentForm'
    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.captcha.CompactCommentForm'

    CAPTCHA_NOISE_FUNCTIONS = ()
    CAPTCHA_FONT_SIZE = 30
    CAPTCHA_LETTER_ROTATION = (-10,10)

    INSTALLED_APPS += (
        'captcha',
    )

.. warning::

    Note that both django-simple-captcha_ and django-recaptcha_ use the same "captcha" module name.
    These packages can't be installed together.


.. _django-nocaptcha-recaptcha: https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha
.. _django-recaptcha: https://github.com/praekelt/django-recaptcha
.. _django-simple-captcha: https://github.com/mbi/django-simple-captcha
