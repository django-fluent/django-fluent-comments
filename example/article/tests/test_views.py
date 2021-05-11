import json
import time

from akismet import Akismet
from django.test import TestCase
from django.urls import reverse
from django_comments import get_model as get_comment_model, signals
from django_comments.forms import CommentForm
from unittest.mock import patch

from article.models import Article
from article.tests import factories
from fluent_comments.moderation import get_model_moderator
from fluent_comments.tests.utils import MockedResponse, override_appsettings


class ViewTests(TestCase):
    def test_get_article_with_comment(self):
        """
        See if the comment renders
        """
        article = factories.create_article()
        comment = factories.create_comment(article=article, comment="Test-Comment")

        response = self.client.get(reverse("article-details", kwargs={"slug": article.slug}))
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
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertContains(response, "Testing comment", status_code=200)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content.decode("utf-8"))
        self.assertTrue(json_response["success"])
        self.assertEqual(json_response["errors"], {})
        self.assertIn("Testing name", json_response["html"])

    @override_appsettings(
        AKISMET_API_KEY="FOOBAR",
        FLUENT_COMMENTS_AKISMET_ACTION="soft_delete",
        FLUENT_CONTENTS_USE_AKISMET=True,
    )
    def test_comment_post_moderated(self):
        """
        See that soft delete works properly.
        """
        # Double check preconditions for moderation
        self.assertIsNotNone(get_model_moderator(Article))
        self.assertTrue(len(signals.comment_will_be_posted.receivers))
        self.assertEqual(
            id(get_comment_model()), signals.comment_will_be_posted.receivers[0][0][1]
        )

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

        for url, is_ajax in [
            (reverse("comments-post-comment-ajax"), True),
            (reverse("comments-post-comment"), False),
        ]:
            with patch.object(Akismet, "_request", return_value=MockedResponse(True)) as m:
                response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(m.call_count, 1, "Moderator not called by " + url)

            if is_ajax:
                self.assertContains(response, "Testing comment", status_code=200)
                self.assertEqual(response.status_code, 200)

                json_response = json.loads(response.content.decode("utf-8"))
                self.assertTrue(json_response["success"])
                self.assertEqual(json_response["errors"], {})
            else:
                self.assertRedirects(response, reverse("comments-comment-done") + "?c=1")

            comment = get_comment_model().objects.filter(user_email="test@email.com")[0]
            self.assertFalse(comment.is_public, "Not moderated by " + url)
            self.assertTrue(comment.is_removed)

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
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content.decode("utf-8"))
        self.assertFalse(json_response["success"])
        self.assertEqual(set(json_response["errors"].keys()), set(["name", "email", "comment"]))

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
        headers = dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        # No data
        self.assertEqual(self.client.post(url, {}, **headers).status_code, 400)

        # invalid pk
        post_data = correct_data.copy()
        post_data["object_pk"] = 999
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)

        # invalid content type
        post_data = correct_data.copy()
        post_data["content_type"] = "article.foo"
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)

        # invalid security hash
        post_data = correct_data.copy()
        post_data["timestamp"] = 0
        self.assertEqual(self.client.post(url, post_data, **headers).status_code, 400)
