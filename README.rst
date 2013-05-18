Introduction
============

The *django-fluent-comments* module enhances the default appearance
of the django.contrib.comments_ application to be directly usable in web sites.
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

First install the module, preferably in a virtual environment. It can be installed from PyPI::

    pip install django-fluent-comments

Or the current folder can be installed::

    pip install .

Configuration
-------------

To use comments, the following settings are required::

    INSTALLED_APPS += (
        'fluent_comments',
        'crispy_forms',
        'django.contrib.comments',
    )

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

The templates which django.contrib.comments_ renders use a single base template for all layouts.
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
which contain the ``content`` and ``title`` blocks that django.contrib.comments_ needs to see.
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


Contributing
------------

This module is designed to be generic, and easy to plug into your site.
In case there is anything you didn't like about it, or think it's not
flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)


.. _django.contrib.comments: https://docs.djangoproject.com/en/dev/ref/contrib/comments/
.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org/
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
.. _Akismet: http://akismet.com
.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
.. _`Uni-form`: http://sprawsm.com/uni-form
