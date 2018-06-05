django-fluent-comments
======================

.. image:: https://travis-ci.org/django-fluent/django-fluent-comments.svg?branch=master
    :target: http://travis-ci.org/django-fluent/django-fluent-comments
.. image:: https://img.shields.io/pypi/v/django-fluent-comments.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/pypi/l/django-fluent-comments.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/codecov/c/github/django-fluent/django-fluent-comments/master.svg
    :target: https://codecov.io/github/django-fluent/django-fluent-comments?branch=master

The *django-fluent-comments* module enhances the default appearance of
the django_comments_ application to be directly usable in web sites.

Features:

* Ajax-based preview and posting of comments
* Configurable and flexible form layouts.
* Comment moderation, with auto-closing / auto-moderation after N days.
* E-mail notification to the site managers of new comments.
* Optional threaded comments support via django-threadedcomments_.
* Optional Akismet_ integration for spam detection.
* Optional reCAPTCHA2 support via django-recaptcha_ or django-nocaptcha-recaptcha_.
* Optional simple captcha support via django-simple-captcha_.

The application is designed to be plug&play;
installing it should already give a better comment layout.

Installation
============

First install the module and django_comments, preferably in a virtual environment::

    pip install django-fluent-comments

Configuration
-------------

Please follow the documentation at https://django-fluent-comments.readthedocs.io/


Contributing
============

This module is designed to be generic, and easy to plug into your site.
In case there is anything you didn't like about it, or think it's not
flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)


.. _django_comments: https://github.com/django/django-contrib-comments
.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org/
.. _django-nocaptcha-recaptcha: https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha
.. _django-recaptcha: https://github.com/praekelt/django-recaptcha
.. _django-simple-captcha: https://github.com/mbi/django-simple-captcha
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
.. _Akismet: http://akismet.com
