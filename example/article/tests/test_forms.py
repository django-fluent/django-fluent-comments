import fluent_comments
from article.tests.utils import override_appsettings, CommentTestCase
from crispy_forms.layout import Row
from fluent_comments.forms.compact import CompactCommentForm


class FormTests(CommentTestCase):

    @override_appsettings(
        FLUENT_COMMENTS_FORM_CLASS='fluent_comments.forms.compact.CompactCommentForm',
        FLUENT_COMMENTS_FIELD_ORDER=(),
        FLUENT_COMMENTS_COMPACT_FIELDS=('name', 'email'),
    )
    def test_form_class(self):
        """
        Test how overriding the form class works.
        """
        form_class = fluent_comments.get_form()
        self.assertIs(form_class, CompactCommentForm)

        form = form_class(self.article)
        self.assertEqual([f.name for f in form.visible_fields()], ['name', 'email', 'url', 'comment', 'honeypot'])
        self.assertEqual(form.helper.layout.fields[3], 'security_hash')
        self.assertIsInstance(form.helper.layout.fields[4], Row)
        self.assertEqual(form.helper.layout.fields[5], 'comment')
        self.assertEqual(form.helper.layout.fields[6], 'honeypot')

    @override_appsettings(
        FLUENT_COMMENTS_FIELD_ORDER=('comment', 'name', 'email', 'url'),
        FLUENT_COMMENTS_COMPACT_FIELDS=('name', 'email'),
    )
    def test_compact_ordering1(self):
        """
        Test how field ordering works.
        """
        form = CompactCommentForm(self.article)
        self.assertEqual([f.name for f in form.visible_fields()], ['comment', 'name', 'email', 'url', 'honeypot'])
        self.assertEqual(list(form.fields.keys()), ['content_type', 'object_pk', 'timestamp', 'security_hash', 'comment', 'name', 'email', 'url', 'honeypot'])
        self.assertEqual(form.helper.layout.fields[3], 'security_hash')
        self.assertEqual(form.helper.layout.fields[4], 'comment')
        self.assertIsInstance(form.helper.layout.fields[5], Row)
        self.assertEqual(form.helper.layout.fields[6], 'honeypot')
