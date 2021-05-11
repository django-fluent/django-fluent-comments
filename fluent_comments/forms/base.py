from collections import OrderedDict

import django_comments
from django.core.exceptions import ImproperlyConfigured
from fluent_comments import appsettings
from fluent_comments.forms.helper import CommentFormHelper
from fluent_comments.forms.helper import (
    SubmitButton,
    PreviewButton,
)  # noqa, import at old class location too

if appsettings.USE_THREADEDCOMMENTS:
    from threadedcomments.forms import ThreadedCommentForm as base_class
else:
    from django_comments.forms import CommentForm as base_class


class AbstractCommentForm(base_class):
    """
    The comment form, applies various settings.
    """

    #: Helper for {% crispy %} template tag
    helper = CommentFormHelper()

    def __init__(self, *args, **kwargs):
        self.is_preview = kwargs.pop("is_preview", False)
        super().__init__(*args, **kwargs)

        # Remove fields from the form.
        # This has to be done in the constructor, because the ThreadedCommentForm
        # inserts the title field in the __init__, instead of the static form definition.
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            try:
                self.fields.pop(name)
            except KeyError:
                raise ImproperlyConfigured(
                    "Field name '{0}' in FLUENT_COMMENTS_EXCLUDE_FIELDS is invalid, "
                    "it does not exist in the '{1}' class.".format(name, self.__class__.__name__)
                )

        if appsettings.FLUENT_COMMENTS_FIELD_ORDER:
            ordering = (
                CommentFormHelper.BASE_FIELDS_TOP
                + appsettings.FLUENT_COMMENTS_FIELD_ORDER
                + CommentFormHelper.BASE_FIELDS_END
            )
            self._reorder_fields(ordering)

    def _reorder_fields(self, ordering):
        new_fields = OrderedDict()
        for name in ordering:
            new_fields[name] = self.fields[name]
        self.fields = new_fields

    def get_comment_model(self):
        # Provide the model used for comments. When this doesn't match
        # the sender used by django_comments.moderation.Moderator used in
        # `comment_will_be_posted.connect(..., sender=...)`, it will break moderation.
        #
        # Since ThreadedCommentForm overrides this method, it breaks moderation
        # with COMMENTS_APP="fluent_comments". Hence, by default let this match
        # the the model the app is configured with.
        return django_comments.get_model()

    def get_comment_create_data(self, *args, **kwargs):
        # Fake form data for excluded fields, so there are no KeyError exceptions
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            self.cleaned_data[name] = ""

        # Pass args, kwargs for django-contrib-comments 1.8, which accepts a ``site_id`` argument.
        return super().get_comment_create_data(*args, **kwargs)
