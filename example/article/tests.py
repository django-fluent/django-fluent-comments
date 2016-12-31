import json
from functools import wraps

import time
import fluent_comments
from crispy_forms.layout import Row
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import timezone
from fluent_comments import appsettings
from fluent_comments import get_model as get_comment_model
from fluent_comments.compat import CommentForm
from article.models import Article
from fluent_comments.forms.compact import CompactCommentForm


def override_appsettings(**settings):
    """
    Temporary override the appsettings.
    """
    def _dec(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            # Apply new settings, backup old, clear caches
            old_values = {}
            for key, new_value in settings.items():
                old_values[key] = getattr(appsettings, key)
                setattr(appsettings, key, new_value)
            fluent_comments.form_class = None
            fluent_comments.model_class = None

            func(*args, **kwargs)
            for key, old_value in old_values.items():
                setattr(appsettings, key, old_value)

            # reset caches
            fluent_comments.form_class = None
            fluent_comments.model_class = None
        return _inner
    return _dec


class CommentsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(CommentsTests, cls).setUpClass()
        Comment = get_comment_model()

        now = timezone.now()
        cls.site = Site.objects.get(pk=1)
        cls.admin = User.objects.create_superuser('superuser', 'myemail@test.com', 'secret')
        cls.article = Article.objects.create(
            title="Testing article",
            slug="testing-article",
            content="This is testing article",
            publication_date=now,
            enable_comments=True,
        )
        cls.article_ctype = ContentType.objects.get_for_model(cls.article)
        cls.comment = Comment.objects.create(
            content_type=cls.article_ctype,
            object_pk=cls.article.pk,
            user=cls.admin,
            user_name="Test-Name",
            user_email="test@example.com",
            user_url="http://example.com",
            comment="Test-Comment",
            submit_date=now,
            site=cls.site,
            is_public=True,
            is_removed=False,
        )

    def test_admin_comments_access(self):
        """
        See that the admin renders
        """
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, ">Test-Name<", status_code=200)

    def test_get_article_with_comment(self):
        """
        See if the comment renders
        """
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Test-Comment", status_code=200)

    def test_comment_post(self):
        """
        Make an ajax post.
        """
        content_type = "article.article"
        timestamp = str(int(time.time()))
        form = CommentForm(self.article)
        security_hash = form.generate_security_hash(content_type, str(self.article.pk), timestamp)
        post_data = {
            "content_type": content_type,
            "object_pk": self.article.pk,
            "name": "Testing name",
            "email": "test@email.com",
            "comment": "Testing comment",
            "timestamp": timestamp,
            "security_hash": security_hash,
        }
        url = reverse("comments-post-comment-ajax")
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, "Testing comment", status_code=200)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content.decode("utf-8"))
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['errors'], {})
        self.assertIn('Testing name', json_response['html'])

    def test_comment_post_missing(self):
        """
        Make an ajax post.
        """
        content_type = "article.article"
        timestamp = str(int(time.time()))
        form = CommentForm(self.article)
        security_hash = form.generate_security_hash(content_type, str(self.article.pk), timestamp)
        post_data = {
            "content_type": content_type,
            "object_pk": self.article.pk,
            "timestamp": timestamp,
            "security_hash": security_hash,
        }
        url = reverse("comments-post-comment-ajax")
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content.decode("utf-8"))
        self.assertFalse(json_response['success'])
        self.assertEqual(list(json_response['errors'].keys()), ['name', 'email', 'comment'])

    def test_comment_post_bad_requests(self):
        """
        See how error handling works on bad requests
        """
        content_type = "article.article"
        timestamp = str(int(time.time()))
        form = CommentForm(self.article)
        security_hash = form.generate_security_hash(content_type, str(self.article.pk), timestamp)
        correct_data = {
            "content_type": content_type,
            "object_pk": self.article.pk,
            "timestamp": timestamp,
            "security_hash": security_hash,
        }
        url = reverse("comments-post-comment-ajax")
        headers = dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # No data
        self.assertEqual(self.client.post(url, {}, **headers).status_code, 400)

        # invalid pk
        post_data = correct_data.copy()
        post_data['object_pk'] = 999
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)

        # invalid content type
        post_data = correct_data.copy()
        post_data['content_type'] = 'article.foo'
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)

        # invalid security hash
        post_data = correct_data.copy()
        post_data['timestamp'] = 0
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)

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
