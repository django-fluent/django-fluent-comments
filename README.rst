Introduction
============

The *django-fluent-comments* module enhances the default appearance
of the *django.contrib.comments* application to be directly usable in web sites.

The application is designed to be plug&play.
It leverages django-crispy-forms_ to handle the form layout.

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

Provide a template that displays the comments for the ``object``::

    {% load comments %}

    {% render_comment_list for object %}
    {% render_comment_form for object %}

The database can be created afterwards::

    ./manage.py syncdb
    ./manage.py runserver


CSS form layout
---------------

A form layout is something that is very different across web sites.
However, this module uses django-crispy-forms_ for the form HTML layout, to make it easy to
have a consistent layout across all your Django forms (in fact, we would encourage to adopt django-crispy-forms_ for all your form layouts).

Currently this module gives you 2 options for the layout:

* `Bootstrap`_ The default template pack. The popular simple and flexible HTML, CSS, and Javascript for user interfaces from Twitter.
* `Uni-form`_ Nice looking, well structured, highly customizable, accessible and usable forms.

The ``CRISPY_TEMPLATE_PACK`` setting allows you to choose which layout you like to use.
For more information, see the django-crispy-forms_ documentation..

If your form CSS framework is not supported, you can create a template pack
for it and submit a pull request to the django-crispy-forms_ authors for inclusion.


Treaded comments
----------------

There is rudimentary support for `django-threadedcomments`_ in this module,
which can be enabled with the following settings::

    INSTALLED_APPS += (
        'threadedcomments',
    )

    COMMENTS_APP = 'threadedcomments'

Note however, that some improvements to django-treadedcomments_ are still open
(see `pull request #39 <https://github.com/HonzaKral/django-threadedcomments/pull/39>`_)
and until that moment it is not possible to take full advantage of the treaded display.


Contributing
------------

This module is designed to be generic, and easy to plug into your site.
In case there is anything you didn't like about it, or think it's not
flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)


.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org/
.. _`Uni-form`: http://sprawsm.com/uni-form
.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
