from __future__ import unicode_literals

import json
import time

from akismet import Akismet
from django.test import TestCase
from django_comments import get_model as get_comment_model, signals
from django_comments.forms import CommentForm
from mock import patch

from article.models import Article
from article.tests import factories
from fluent_comments.moderation import get_model_moderator
from fluent_comments.tests.utils import MockedResponse, override_appsettings
try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse


class ViewTests(TestCase):

    def test_get_article_with_comment(self):
        """
        See if the comment renders
        """
        article = factories.create_article()
        comment = factories.create_comment(article=article, comment="Test-Comment")

        response = self.client.get(reverse('article-details', kwargs={"slug": article.slug}))
        self.assertContains(response, "Test-Comment", status_code=200)

    def test_comment_post(self):
        """
        Make an ajax post.
        """
        content_type = "article.article"
        timestamp = str(int(time.time()))
        article = factories.create_article()

        form = CommentForm(article)
        security_hash = form.generate_security_hash(content_type, str(article.pk), timestamp)
        post_data = {
            "content_type": content_type,
            "object_pk": article.pk,
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
        article = factories.create_article()

        form = CommentForm(article)
        security_hash = form.generate_security_hash(content_type, str(article.pk), timestamp)
        post_data = {
            "content_type": content_type,
            "object_pk": article.pk,
            "timestamp": timestamp,
            "security_hash": security_hash,
        }
        url = reverse("comments-post-comment-ajax")
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content.decode("utf-8"))
        self.assertFalse(json_response['success'])
        self.assertEqual(set(json_response['errors'].keys()), set(['name', 'email', 'comment']))

    def test_comment_post_bad_requests(self):
        """
        See how error handling works on bad requests
        """
        content_type = "article.article"
        timestamp = str(int(time.time()))
        article = factories.create_article()

        form = CommentForm(article)
        security_hash = form.generate_security_hash(content_type, str(article.pk), timestamp)
        correct_data = {
            "content_type": content_type,
            "object_pk": article.pk,
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
