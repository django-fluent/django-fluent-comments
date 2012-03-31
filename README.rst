Introduction
============

The *django-fluent-comments* module enhances the default appearance
of the *django.contrib.comments* application to be directly usable in web sites.

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
        'django.contrib.comments',
    )

Optionally, `django-threadedcomments`_ can be included::

    INSTALLED_APPS += (
        'threadedcomments',
    )

    COMMENTS_APP = 'threadedcomments'

Add the following in ``urls.py``::

    urlpatterns += patterns('',
        url(r'^blog/comments/', include('fluent_comments.urls')),
    )

Provide a template that displays the comments for the ``object``::

    {% load comments %}

    {% render_comment_list for object %}
    {% render_comment_form for object %}

The database can be created afterwards::

    ./manage.py syncdb
    ./manage.py runserver


.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git

