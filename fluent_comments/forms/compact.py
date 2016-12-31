"""

"""
from crispy_forms.layout import Layout, Row, Column
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property

from fluent_comments import appsettings
from fluent_comments.forms.base import AbstractCommentForm, CommentFormHelper, SubmitButton, PreviewButton


class CompactCommentForm(AbstractCommentForm):
    """
    A form with a very compact layout;
    all the name/email/phone fields are displayed in a single top row.
    It uses Bootstrap 3 layout by default to generate the columns.
    """
    top_row_fields = appsettings.FLUENT_COMMENTS_COMPACT_FIELDS
    top_row_columns = appsettings.FLUENT_COMMENTS_COMPACT_GRID_SIZE
    top_column_class = appsettings.FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS

    @cached_property
    def helper(self):
        # As extra service, auto-adjust the layout based on the project settings.
        # This allows defining the top-row, and still get either 2 or 3 columns
        top_fields = [name for name in self.fields.keys() if name in self.top_row_fields]
        other_fields = [name for name in self.fields.keys() if name not in self.top_row_fields]
        col_size = int(self.top_row_columns / len(top_fields))
        col_class = self.top_column_class.format(size=col_size)

        compact_row = Row(*[Column(name, css_class=col_class) for name in top_fields])

        if appsettings.FLUENT_COMMENTS_FIELD_ORDER:
            # The fields are already ordered by the AbstractCommentForm.__init__ method.
            # See whether the top row should be before all other fields.
            other_index = 999
            top_index = 999
            for name in appsettings.FLUENT_COMMENTS_FIELD_ORDER:
                try:
                    other_index = min(other_index, other_fields.index(name))
                except ValueError:
                    try:
                        top_index = min(top_index, top_fields.index(name))
                    except ValueError:
                        raise ImproperlyConfigured("FLUENT_COMMENTS_FIELD_ORDER value {0} does not a valid comment field".format(
                            name
                        ))
            if top_index <= other_index:
                new_fields = compact_row + other_fields
            else:
                new_fields = other_fields + compact_row
        else:
            new_fields = compact_row + other_fields

        helper = CommentFormHelper()
        helper.form_class = helper.form_class.replace('form-horizontal', 'form-vertical') + ' comments-form-compact'
        helper.label_class = 'sr-only'
        helper.field_class = ''
        helper.layout = Layout(*new_fields)
        helper.add_input(SubmitButton())
        helper.add_input(PreviewButton())
        return helper

    def __init__(self, *args, **kwargs):
        super(CompactCommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = u"{0}:".format(field.label)
