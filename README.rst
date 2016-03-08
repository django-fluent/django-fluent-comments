django-fluent-comments
======================

.. image:: https://travis-ci.org/edoburu/django-fluent-comments.svg?branch=master
    :target: http://travis-ci.org/edoburu/django-fluent-comments
.. image:: https://img.shields.io/pypi/v/django-fluent-comments.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/pypi/dm/django-fluent-comments.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/badge/wheel-yes-green.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/pypi/l/django-fluent-comments.svg
    :target: https://pypi.python.org/pypi/django-fluent-comments/
.. image:: https://img.shields.io/codecov/c/github/edoburu/django-fluent-comments/master.svg
    :target: https://codecov.io/github/edoburu/django-fluent-comments?branch=master

The *django-fluent-comments* module enhances the default appearance
of the django_comments_ or django.contrib.comments_ application to be directly usable in web sites.
The features are:

* Ajax-based preview and posting of comments
* Configurable form layouts using django-crispy-forms_ and settings to exclude fields.
* Comment moderation, using Akismet_ integration and auto-closing after N days.
* E-mail notification to the site managers of new comments.
* Optional threaded comments support via django-threadedcomments_.

The application is designed to be plug&play;
installing it should already give a better comment layout.

Installation
============

First install the module and django_comments, preferably in a virtual environment. It can be installed from PyPI::

    pip install django-fluent-comments

Or the current folder can be installed::

    pip install .

Configuration
-------------

To use comments, the following settings are required::

    INSTALLED_APPS += (
        'fluent_comments',
        'crispy_forms',
        'django_comments',
        'django.contrib.sites',
    )

    COMMENTS_APP = 'fluent_comments'

.. note::
   For older Django versions (up till 1.7), you can also use django.contrib.comments_ in the ``INSTALLED_APPS``.
   This packages uses either of those packages, depending on what is installed.

Add the following in ``urls.py``::

    urlpatterns += patterns('',
        url(r'^blog/comments/', include('fluent_comments.urls')),
    )

Provide a template that displays the comments for the ``object`` and includes the required static files::

    {% load comments %}

    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}fluent_comments/css/ajaxcomments.css" />
    <script type="text/javascript" src="{{ STATIC_URL }}fluent_comments/js/ajaxcomments.js"></script>

    {% render_comment_list for object %}
    {% render_comment_form for object %}

The database can be created afterwards::

    ./manage.py syncdb
    ./manage.py runserver

Template for non-ajax pages
---------------------------

The templates which django_comments_ renders use a single base template for all layouts.
This template is empty by default since it's only serves as a placeholder.
To complete the configuration of the comments module, create a ``comments/base.html`` file
that maps the template blocks onto your website base template. For example::

    {% extends "mysite/base.html" %}{% load i18n %}

    {% block headtitle %}{% block title %}{% trans "Responses for page" %}{% endblock %}{% endblock %}

    {% block main %}
        <div id="comments-wrapper">
            {% block content %}{% endblock %}
        </div>
    {% endblock %}

In this example, the base template has a ``headtitle`` and ``main`` block,
which contain the ``content`` and ``title`` blocks that django_comments_ needs to see.
This application also outputs an ``extrahead`` block for a meta-refresh tag.
The ``extrahead`` block can be included in the site base template directly,
so it doesn't have to be included in the ``comments/base.html`` file.


CSS form layout
---------------

Form layouts generally differ across web sites, hence this application doesn't dictate a specific form layout.
Instead, this application uses django-crispy-forms_ which allows configuration of the form appearance.
By default, the forms can be rendered with 2 well known CSS frameworks:

* `Bootstrap`_ The default template pack. The popular simple and flexible HTML, CSS, and Javascript for user interfaces from Twitter.
* `Uni-form`_ Nice looking, well structured, highly customizable, accessible and usable forms.

The ``CRISPY_TEMPLATE_PACK`` setting can be used to switch between both layouts.
For more information, see the django-crispy-forms_ documentation.

Both CSS frameworks have a wide range of themes available, which should give a good head-start to have a good form layout.
In fact, we would encourage to adopt django-crispy-forms_ for all your applications to have a consistent layout across all your Django forms.

If your form CSS framework is not supported, you can create a template pack
for it and submit a pull request to the django-crispy-forms_ authors for inclusion.


Hiding form fields
~~~~~~~~~~~~~~~~~~

Form fields can be hidden using the following settings::

    FLUENT_COMMENTS_EXCLUDE_FIELDS = ('name', 'email', 'url')
    COMMENTS_APP = 'fluent_comments'

When `django-threadedcomments`_ in used, the ``title`` field can also be removed.


Comment moderation
------------------

Comment moderation can be enabled for the specific models using::


    from fluent_comments.moderation import moderate_model
    from myblog.models import BlogPost

    moderate_model(BlogPost,
        publication_date_field='publication_date',
        enable_comments_field='enable_comments',
    )

This code can be placed in a ``models.py`` file.
The provided field names are optional. By providing the field names,
the comments can be auto-moderated or auto-closed after a number of days since the publication date.

The following settings are available for comment moderation::

    AKISMET_API_KEY = "your-api-key"
    AKISMET_BLOG_URL = "http://example.com"        # Optional, to override auto detection
    AKISMET_IS_TEST = False                        # Enable to make test runs

    FLUENT_CONTENTS_USE_AKISMET = True             # Enabled by default when AKISMET_API_KEY is set.
    FLUENT_COMMENTS_CLOSE_AFTER_DAYS = None        # Auto-close comments after N days
    FLUENT_COMMENTS_MODERATE_AFTER_DAYS = None     # Auto-moderate comments after N days.
    FLUENT_COMMENTS_AKISMET_ACTION = 'moderate'    # Set to 'moderate' or 'delete'

To use Akismet_ moderation, make sure the ``AKISMET_API_KEY`` setting is defined.

Python 3 notes
~~~~~~~~~~~~~~

The ``akismet`` 0.2 release does not support Python 3.
Hence, it's only installed for Python 2 environments.

For Python 3 systems, install one of the forks from the Akismet_ library
to have proper Python 3 support. For example by including the following in your ``requirements.txt``::

    -e git+https://github.com/allieus/python-akismet.git#egg=akismet


E-mail notification
-------------------

By default, the ``MANAGERS`` of a Django site will receive an e-mail notification of new comments.
This feature can be enabled or disabled using::

    FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = True

The template ``comments/comment_notification_email.txt`` is used to generate the e-mail message.


Threaded comments
-----------------

There is build-in support for django-threadedcomments_ in this module.
It can be enabled using the following settings::

    INSTALLED_APPS += (
        'threadedcomments',
    )

    COMMENTS_APP = 'fluent_comments'

The templates and admin interface adapt themselves automatically
to show the threaded comments.


IP-Address detection
--------------------

This package stores the remote IP of the visitor in the model, and passes it to Akismet_.
The IP Address is read from the ``REMOTE_ADDR`` meta field.
In case your site is behind a HTTP proxy (e.g. using Gunicorn or a load balancer),
this would make all comments appear to be posted from the load balancer IP.

The best and most secure way to fix this, is using WsgiUnproxy_ middleware in your ``wsgi.py``:

.. code-block:: python

    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from wsgiunproxy import unproxy

    application = get_wsgi_application()
    application = unproxy(trusted_proxies=settings.TRUSTED_X_FORWARDED_FOR_IPS)(application)

In your ``settings.py``, you can define which hosts may pass the ``X-Forwarded-For``
header in the HTTP request. For example:

.. code-block:: python

    TRUSTED_X_FORWARDED_FOR_IPS = (
        '11.22.33.44',
        '192.168.0.1',
    )


Contributing
------------

This module is designed to be generic, and easy to plug into your site.
In case there is anything you didn't like about it, or think it's not
flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)


.. _django_comments: https://github.com/django/django-contrib-comments
.. _django.contrib.comments: https://docs.djangoproject.com/en/1.7/ref/contrib/comments/
.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org/
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
.. _Akismet: http://akismet.com
.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
.. _`Uni-form`: http://sprawsm.com/uni-form
.. _WsgiUnproxy: https://pypi.python.org/pypi/WsgiUnproxy
