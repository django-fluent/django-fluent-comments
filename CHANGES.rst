New in development version
--------------------------

* Support multiple comment area's in the same page.
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

.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org
.. _django-threadedcomments: https://github.com/HonzaKral/django-threadedcomments.git
