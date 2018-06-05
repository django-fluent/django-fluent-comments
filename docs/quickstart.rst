Installation
============

First install the module and django_comments, preferably in a virtual environment::

    pip install django-fluent-comments

Configuration
-------------

To use comments, the following settings are required:

.. code-block:: python

    INSTALLED_APPS += (
        'fluent_comments',  # must be before django_comments
        'crispy_forms',
        'django_comments',
        'django.contrib.sites',
    )

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    COMMENTS_APP = 'fluent_comments'

Add the following in ``urls.py``:

.. code-block:: python

    urlpatterns += patterns('',
        url(r'^blog/comments/', include('fluent_comments.urls')),
    )

The database can be created afterwards:

.. code-block:: bash

    ./manage.py migrate

Usage in the page
-----------------

Provide a template that displays the comments for the ``object`` and includes the required static files:

.. code-block:: html+django

    {% load comments static %}

    <link rel="stylesheet" type="text/css" href="{% static 'fluent_comments/css/ajaxcomments.css' %}" />
    <script type="text/javascript" src="{% static 'fluent_comments/js/ajaxcomments.js' %}"></script>

    {% render_comment_list for object %}
    {% render_comment_form for object %}

.. note::

    When using the comment module via django-fluent-contents_ or django-fluent-blogs_,
    this step can be omitted.

Template for non-ajax pages
---------------------------

The templates which django_comments_ renders use a single base template for all layouts.
This template is empty by default since it's only serves as a placeholder.
To complete the configuration of the comments module, create a ``comments/base.html`` file
that maps the template blocks onto your website base template. For example:

.. code-block:: html+django

    {% extends "mysite/base.html" %}{% load i18n %}

    {% block meta-title %}{% block title %}{% trans "Responses for page" %}{% endblock %}{% endblock %}

    {% block main %}
        <div id="comments-wrapper">
            {% block content %}{% endblock %}
        </div>
    {% endblock %}

In this example, the base template has a ``meta-title`` and ``main`` block,
which contain the ``content`` and ``title`` blocks that django_comments_ needs to see.
This application also outputs an ``extrahead`` block for a meta-refresh tag.
The ``extrahead`` block can be included in the site base template directly,
so it doesn't have to be included in the ``comments/base.html`` file.

.. _django_comments: https://github.com/django/django-contrib-comments
.. _django-fluent-blogs: https://github.com/django-fluent/django-fluent-blogs
.. _django-fluent-contents: https://github.com/django-fluent/django-fluent-contents
