from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from fluent_comments.compat import CommentForm
from freezegun import freeze_time
from article.models import Article


class CommentsTests(TestCase):
    fixtures = ["data", ]

    def setUp(self):
        self.admin = User.objects.create_superuser('superuser', 'myemail@test.com', 'secret')

    def test_admin_comments_access(self):
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    @freeze_time("2016-01-04 17:00:00")
    def test_comment_post(self):
        content_type = "article.article"
        object_pk = "1"
        timestamp = "1451919617"
        form = CommentForm(Article())
        security_hash = form.generate_security_hash(content_type, object_pk, timestamp)
        post_data = {
            "content_type": content_type,
            "object_pk": object_pk,
            "name": "Testing name",
            "email": "test@email.com",
            "comment": "Testing comment",
            "timestamp": timestamp,
            "security_hash": security_hash,
        }
        response = self.client.post(reverse("comments-post-comment-ajax"), post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, "Testing comment", status_code=200)
        self.assertEqual(response.status_code, 200, response.content.decode("utf-8"))
