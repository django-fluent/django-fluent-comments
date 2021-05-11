from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django_comments import get_model as get_comments_model
from django_comments.managers import CommentManager

from fluent_comments import appsettings

if appsettings.USE_THREADEDCOMMENTS:
    from threadedcomments.models import ThreadedComment as BaseModel
else:
    from django_comments.models import Comment as BaseModel


class FluentCommentManager(CommentManager):
    """
    Manager to optimize SQL queries for comments.
    """

    def get_queryset(self):
        return super().get_queryset().select_related("user")


class FluentComment(BaseModel):
    """
    Proxy model to make sure that a ``select_related()`` is performed on the ``user`` field.
    """

    objects = FluentCommentManager()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        proxy = True
        managed = False


def get_comments_for_model(content_object, include_moderated=False):
    """
    Return the QuerySet with all comments for a given model.
    """
    qs = get_comments_model().objects.for_model(content_object)

    if not include_moderated:
        qs = qs.filter(is_public=True, is_removed=False)

    return qs


class CommentsRelation(GenericRelation):
    """
    A :class:`~django.contrib.contenttypes.generic.GenericRelation` which can be applied to a parent model that
    is expected to have comments. For example:

    .. code-block:: python

        class Article(models.Model):
            comments_set = CommentsRelation()
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            to=get_comments_model(),
            content_type_field="content_type",
            object_id_field="object_pk",
            **kwargs
        )
