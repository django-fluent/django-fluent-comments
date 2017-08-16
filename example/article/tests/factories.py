from random import random

from article.models import Article
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django_comments import get_model as get_comment_model


def create_article(**kwargs):
    """
    Create an article, with default parameters
    """
    defaults = dict(
        title="Testing article",
        slug="testing-article" + str(random()),
        content="This is testing article",
        publication_date=now(),
        enable_comments=True,
    )
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


def create_comment(comment_model=None, article=None, user=None, **kwargs):
    """
    Create a new comment.
    """
    if article is None:
        article = create_article()

    article_ctype = ContentType.objects.get_for_model(article)
    defaults = dict(
        user=user,
        user_name="Test-Name",
        user_email="test@example.com",
        user_url="http://example.com",
        comment="Test-Comment",
        submit_date=now(),
        site=Site.objects.get_current(),
        ip_address='127.0.0.1',
        is_public=True,
        is_removed=False,
    )
    defaults.update(kwargs)

    Comment = comment_model or get_comment_model()
    return Comment.objects.create(
        content_type=article_ctype,
        object_pk=article.pk,
        **defaults
    )
