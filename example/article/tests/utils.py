from functools import wraps
from time import time

import fluent_comments
from article.models import Article
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import timezone
from fluent_comments import appsettings
from fluent_comments import get_model as get_comment_model


class CommentTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(CommentTestCase, cls).setUpClass()
        Comment = get_comment_model()

        now = timezone.now()
        cls.site = Site.objects.get(pk=1)
        cls.admin = User.objects.create_superuser(str(time()), 'myemail@test.com', 'secret')
        cls.article = Article.objects.create(
            title="Testing article",
            slug="testing-article" + str(time()),
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
