Version 1.2.2 (2016-08-29)
--------------------------

* Allow non-integer primary key
* Added Slovak translation


Version 1.2.1 (2016-05-23)
--------------------------

* Fixed error handling in JavaScript when server reports an error.


Version 1.2 (2015-02-03)
------------------------

* Fixed Django 1.9 support.


Version 1.1 (2015-12-28)
------------------------

* Fix Django 1.9 issue with imports.
* Fix error in the admin for non-existing objects.
* Fix Python 3 installation error (dropped Akismet_ requirement).
* Drop Django 1.4 compatibility (in the templates).


Version 1.0.5 (2015-10-17)
--------------------------

* Fix Django 1.9 issue with importing models in ``__init__.py``.
* Fix django-threadedcomments_ 1.0.1 support


Version 1.0.4 (2015-10-01)
--------------------------

* Fixed ``get_comments_model()`` import.


Version 1.0.3 (2015-09-01)
--------------------------

* Fix support for ``TEMPLATE_STRING_IF_INVALID``, avoid parsing the "for" argument in ``{% ajax_comment_tags for object %}``.
* Look for the correct ``#id_parent`` node (in case there are multiple)
* Improve Bootstrap 3 appearance (template can be overwritten).

Version 1.0.2
-------------

* Fixed packaging bug

Version 1.0.1
-------------

* Fix app registry errors in Django 1.7
* Fix security hash formatting errors on bad requests.

Version 1.0.0
-------------

* Added Django 1.8 support, can use either the django_comments_ or the django.contrib.comments_ package now.
* Fixed Python 3 issue in the admin
* Fixed unicode support in for subject of notification email

Released as 1.0b1:
------------------

* Fixed ajax-comment-busy check
* Fixed clearing the whole container on adding comment

Released as 1.0a2:
------------------

* Fix installation at Python 2.6

Released as 1.0a1:
------------------

* Added support for Python 3 (with the exception of Akismet_ support).
* Added support for multiple comment area's in the same page.

  **NOTE:** any custom templates need to be updated, to
  use the new ``id``, ``class`` and ``data-object-id`` attributes.


Version 0.9.2
-------------

* Fix errors in Ajax view, due to a ``json`` variable name conflict
* Fix support for old jQuery and new jQuery (.on vs .live)
* Fix running the example project with Django 1.5
* Fix error messages in ``post_comment_ajax`` view.
* Fix empty user name column in the admin list.
* Fix undesired "reply" link in the preview while using django-threadedcomments_.
* Fix HTML layout of newly added threaded comments.
* Fix Python 3 support


Version 0.9.1
-------------

* Fix running at Django 1.6 alpha 1


Version 0.9
-----------

* Full support for django-threadedcomments_ out of the box.
* Fix CSS class for primary submit button, is now ``.btn-primary``.


Version 0.8.0
-------------

First public release

* Ajax-based preview and posting of comments
* Configurable form layouts using django-crispy-forms_ and settings to exclude fields.
* Comment moderation, using Akismet_ integration and auto-closing after N days.
* E-mail notification to the site managers of new comments.
* Rudimentary support for django-threadedcomments_

.. _Akismet: https://pypi.python.org/pypi/akismet
.. _django_comments: https://github.com/django/django-contrib-comments
.. _django.contrib.comments: https://docs.djangoproject.com/en/1.7/ref/contrib/comments/
.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
