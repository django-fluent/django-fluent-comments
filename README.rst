Introduction
============

The *django-fluent-comments* module enhances the default appearance
of the django.contrib.comments_ application to be directly usable in web sites.
The features are:

* Ajax-based preview and posting of comments
* Configurable form layouts using django-crispy-forms_.

The application is designed to be plug&play;
installing it should already give a better comment layout.

Installation
============

First install the module, preferably in a virtual environment::

    git clone https://github.com/edoburu/django-fluent-comments.git
    cd django-fluent-comments
    pip install .

Configuration
-------------

To use comments, the following settings are required::

    INSTALLED_APPS += (
        'fluent_contents',
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


Threaded comments
-----------------

There is rudimentary support for `django-threadedcomments`_ in this module,
which can be enabled with the following settings::

    INSTALLED_APPS += (
        'threadedcomments',
    )

    COMMENTS_APP = 'threadedcomments'

Note however, that some improvements to django-threadedcomments_ are still open
(see `pull request #39 <https://github.com/HonzaKral/django-threadedcomments/pull/39>`_)
and until that moment it is not easy to take full advantage of the threaded display.


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
.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
.. _`Uni-form`: http://sprawsm.com/uni-form
