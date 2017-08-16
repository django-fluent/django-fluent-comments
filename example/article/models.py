from django.core.urlresolvers import reverse
from django.db import models
from django.utils.six import python_2_unicode_compatible

from fluent_comments.moderation import moderate_model, comments_are_open, comments_are_moderated
from fluent_comments.models import get_comments_for_model, CommentsRelation


@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    content = models.TextField("Content")

    publication_date = models.DateTimeField("Publication date")
    enable_comments = models.BooleanField("Enable comments", default=True)

    # Optional reverse relation, allow ORM querying:
    comments_set = CommentsRelation()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-details', kwargs={'slug': self.slug})

    # Optional, give direct access to moderation info via the model:
    comments = property(get_comments_for_model)
    comments_are_open = property(comments_are_open)
    comments_are_moderated = property(comments_are_moderated)


# Give the generic app support for moderation by django-fluent-comments:
moderate_model(
    Article,
    publication_date_field='publication_date',
    enable_comments_field='enable_comments'
)
