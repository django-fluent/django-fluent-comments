from __future__ import unicode_literals

import json
import time

from article.tests import factories
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_comments.forms import CommentForm


class CommentsTests(TestCase):

    def test_admin_comments_access(self):
        """
        See that the admin renders
        """
        admin = User.objects.create_superuser('admin2', 'admin@example.com', 'secret')
        comment = factories.create_comment(user_name='Test-Name')

        self.client.login(username=admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, ">Test-Name<", status_code=200)

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
