import django
import time
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from django.utils import timezone
from fluent_comments import get_model as get_comment_model
from fluent_comments.compat import CommentForm
from article.models import Article


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
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    def test_comment_post(self):
        content_type = "article.article"
        object_pk = "1"
        timestamp = str(int(time.time()))
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
