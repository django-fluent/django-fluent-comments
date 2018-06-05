.. django-fluent-comments documentation master file, created by
   sphinx-quickstart on Mon Jun  4 23:21:38 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-fluent-comments's documentation!
==================================================

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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   topics/form_layout
   topics/templates
   topics/captcha
   topics/akismet
   topics/email
   topics/moderate
   topics/threaded_comments
   topics/ipaddress
   topics/gdpr
   reference/settings
   releases


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
