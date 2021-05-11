Changing the form layout
========================

Form layouts generally differ across web sites, hence this application doesn't dictate a specific form layout.
Instead, this application uses django-crispy-forms_ which allows configuration of the form appearance.

The defaults are set to Bootstrap 3 layouts, but can be changed.

For example, use:

.. code-block:: python

    CRISPY_TEMPLATE_PACK = 'bootstrap4'


Using a different form class
----------------------------

By choosing a different form class, the form layout can be redefined at once:

The default is:

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.DefaultCommentForm'

    FLUENT_COMMENTS_FORM_CSS_CLASS = 'comments-form form-horizontal'
    FLUENT_COMMENTS_LABEL_CSS_CLASS = 'col-sm-2'
    FLUENT_COMMENTS_FIELD_CSS_CLASS = 'col-sm-10'

You can replace the labels with placeholders using:

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.CompactLabelsCommentForm'

Or place some fields at a single row:

.. code-block:: python

    FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.CompactCommentForm'

    # Optional settings for the compact style:
    FLUENT_COMMENTS_COMPACT_FIELDS = ('name', 'email', 'url')
    FLUENT_COMMENTS_COMPACT_GRID_SIZE = 12
    FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS = "col-sm-{size}"

.. _field-order:

Changing the field order
------------------------

The default is:

.. code-block:: python

    FLUENT_COMMENTS_FIELD_ORDER = ('name', 'email', 'url', 'comment')

For a more modern look, consider placing the comment first:

.. code-block:: python

    FLUENT_COMMENTS_FIELD_ORDER = ('comment', 'name', 'email', 'url')


Hiding form fields
------------------

Form fields can be hidden using the following settings:

.. code-block:: python

    FLUENT_COMMENTS_EXCLUDE_FIELDS = ('name', 'email', 'url')

When :doc:`django-threadedcomments <threaded_comments>` are used, the ``title`` field can also be removed.

.. note::

    Omitting fields from ``FLUENT_COMMENTS_FIELD_ORDER`` has the same effect.


Using a custom form class
-------------------------

When the settings above don't provide the layout you need,
you can define a custom form class entirely:

.. code-block:: python

    from fluent_comments.forms import CompactLabelsCommentForm

    # Or for recaptcha as base, import:
    from fluent_comments.forms.recaptcha import CompactCommentForm


    class CommentForm(CompactLabelsCommentForm):
        """
        The comment form to use
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['url'].label = _("Website")  # Changed the label
            self.fields['email'].label = _("Email address (will not be published)")

And use that class in the ``FLUENT_COMMENTS_FORM_CLASS`` setting.
The ``helper`` attribute defines how the layout is constructed by django-crispy-forms_,
and should be redefined the change the field ordering or appearance.


Switching form templates
------------------------

By default, the forms can be rendered with 2 well known CSS frameworks:

* `Bootstrap`_ The default template pack. The popular simple and flexible HTML, CSS, and Javascript for user interfaces from Twitter.
* `Uni-form`_ Nice looking, well structured, highly customizable, accessible and usable forms.

The ``CRISPY_TEMPLATE_PACK`` setting can be used to switch between both layouts.
For more information, see the django-crispy-forms_ documentation.

Both CSS frameworks have a wide range of themes available, which should give a good head-start to have a good form layout.
In fact, we would encourage to adopt django-crispy-forms_ for all your applications to have a consistent layout across all your Django forms.

If your form CSS framework is not supported, you can create a template pack
for it and submit a pull request to the django-crispy-forms_ authors for inclusion.



.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
.. _`Uni-form`: http://sprawsm.com/uni-form


.. _django-crispy-forms: http://django-crispy-forms.readthedocs.org/
