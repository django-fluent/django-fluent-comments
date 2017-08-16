import fluent_comments
from article.tests import factories
from article.tests.utils import override_appsettings
from crispy_forms.layout import Row
from django.test import TestCase

from fluent_comments import appsettings
from fluent_comments.forms.compact import CompactCommentForm


class FormTests(TestCase):

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

        article = factories.create_article()
        form = form_class(article)

        if appsettings.USE_THREADEDCOMMENTS:
            self.assertEqual([f.name for f in form.visible_fields()], ['name', 'email', 'url', 'title', 'comment', 'honeypot'])
            self.assertEqual(form.helper.layout.fields[3], 'security_hash')
            self.assertIsInstance(form.helper.layout.fields[4], Row)
            self.assertEqual(form.helper.layout.fields[6], 'comment')
            self.assertEqual(form.helper.layout.fields[7], 'honeypot')
        else:
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
        article = factories.create_article()
        form = CompactCommentForm(article)
        self.assertEqual([f.name for f in form.visible_fields()], ['comment', 'name', 'email', 'url', 'honeypot'])
        if appsettings.USE_THREADEDCOMMENTS:
            self.assertEqual(list(form.fields.keys()), [
                'content_type', 'object_pk', 'timestamp', 'security_hash',
                'parent', 'comment', 'name', 'email', 'url', 'honeypot'
            ])

            self.assertEqual(form.helper.layout.fields[3], 'security_hash')
            self.assertEqual(form.helper.layout.fields[5], 'comment')
            self.assertIsInstance(form.helper.layout.fields[6], Row)
            self.assertEqual(form.helper.layout.fields[7], 'honeypot')
        else:
            self.assertEqual(list(form.fields.keys()), [
                'content_type', 'object_pk', 'timestamp', 'security_hash',
                'comment', 'name', 'email', 'url', 'honeypot'
            ])

            self.assertEqual(form.helper.layout.fields[3], 'security_hash')
            self.assertEqual(form.helper.layout.fields[4], 'comment')
            self.assertIsInstance(form.helper.layout.fields[5], Row)
            self.assertEqual(form.helper.layout.fields[6], 'honeypot')
