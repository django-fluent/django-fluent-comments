from crispy_forms.layout import Submit, Button
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from django_comments import get_form_target
from fluent_comments import appsettings

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict  # Python 2.6


if appsettings.USE_THREADEDCOMMENTS:
    from threadedcomments.forms import ThreadedCommentForm as base_class
else:
    from fluent_comments.compat import CommentForm as base_class


class CommentFormHelper(FormHelper):
    """
    The django-crispy-forms configuration that handles form appearance.
    The default is configured to show bootstrap forms nicely.
    """
    form_tag = False  # we need to define the form_tag
    form_id = 'comment-form-ID'
    form_class = 'js-comments-form {0}'.format(appsettings.FLUENT_COMMENTS_FORM_CSS_CLASS)
    label_class = appsettings.FLUENT_COMMENTS_LABEL_CSS_CLASS
    field_class = appsettings.FLUENT_COMMENTS_FIELD_CSS_CLASS
    render_unmentioned_fields = True  # like honeypot and security_hash

    BASE_FIELDS_TOP = ('content_type', 'object_pk', 'timestamp', 'security_hash')
    BASE_FIELDS_END = ('honeypot',)
    BASE_FIELDS = BASE_FIELDS_TOP + BASE_FIELDS_END

    @property
    def form_action(self):
        return get_form_target()  # reads get_form_target from COMMENTS_APP

    def __init__(self, form=None):
        super(CommentFormHelper, self).__init__(form=form)
        if form is not None:
            # When using the helper like this, it could generate all fields.
            self.form_id = 'comment-form-{0}'.format(form.target_object.pk)
            self.attrs = {
                'data-object-id': form.target_object.pk,
            }


class SubmitButton(Submit):
    """
    The submit button to add to the layout.

    Note: the ``name=post`` is mandatory, it helps the
    """

    def __init__(self, text=_("Submit"), **kwargs):
        super(SubmitButton, self).__init__(name='post', value=text, **kwargs)


class PreviewButton(Button):
    """
    The preview button to add to the layout.

    Note: the ``name=post`` is mandatory, it helps the
    """
    input_type = 'submit'

    def __init__(self, text=_("Preview"), **kwargs):
        kwargs.setdefault('css_class', 'btn-default')
        super(PreviewButton, self).__init__(name='preview', value=text, **kwargs)


class AbstractCommentForm(base_class):
    """
    The comment form, applies various settings.
    """

    #: Helper for {% crispy %} template tag
    helper = CommentFormHelper()
    helper.form_tag = False

    def __init__(self, *args, **kwargs):
        super(AbstractCommentForm, self).__init__(*args, **kwargs)

        # Remove fields from the form.
        # This has to be done in the constructor, because the ThreadedCommentForm
        # inserts the title field in the __init__, instead of the static form definition.
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            try:
                self.fields.pop(name)
            except KeyError:
                raise ImproperlyConfigured("Field name '{0}' in FLUENT_COMMENTS_EXCLUDE_FIELDS is invalid, it does not exist in the comment form.")

        if appsettings.FLUENT_COMMENTS_FIELD_ORDER:
            new_fields = OrderedDict()
            ordering = (
                CommentFormHelper.BASE_FIELDS_TOP +
                appsettings.FLUENT_COMMENTS_FIELD_ORDER +
                CommentFormHelper.BASE_FIELDS_END
            )
            for name in ordering:
                new_fields[name] = self.fields[name]
            self.fields = new_fields

    def get_comment_create_data(self):
        # Fake form data for excluded fields, so there are no KeyError exceptions
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            self.cleaned_data[name] = ""

        return super(AbstractCommentForm, self).get_comment_create_data()
