from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django_comments.managers import CommentManager

from fluent_comments import appsettings
from django_comments import get_model as get_comments_model, signals

try:
    from django.contrib.contenttypes.fields import GenericRelation  # Django 1.9+
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.9+
except ImportError:
    from django.contrib.sites.models import get_current_site


if appsettings.USE_THREADEDCOMMENTS:
    from threadedcomments.models import ThreadedComment as BaseModel
else:
    from django_comments.models import Comment as BaseModel


class FluentCommentManager(CommentManager):
    """
    Manager to optimize SQL queries for comments.
    """

    def get_queryset(self):
        return super(CommentManager, self).get_queryset().select_related('user')


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


@receiver(signals.comment_was_posted)
def on_comment_posted(sender, comment, request, **kwargs):
    """
    Send email notification of a new comment to site staff when email notifications have been requested.
    """
    # This code is copied from django_comments.moderation.
    # That code doesn't offer a RequestContext, which makes it really
    # hard to generate proper URL's with FQDN in the email
    #
    # Instead of implementing this feature in the moderator class, the signal is used instead
    # so the notification feature works regardless of a manual moderator.register() call in the project.
    if not appsettings.FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION:
        return

    recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
    site = get_current_site(request)
    content_object = comment.content_object

    if comment.is_removed:
        subject = u'[{0}] Spam comment on "{1}"'.format(site.name, content_object)
    elif not comment.is_public:
        subject = u'[{0}] Moderated comment on "{1}"'.format(site.name, content_object)
    else:
        subject = u'[{0}] New comment posted on "{1}"'.format(site.name, content_object)

    context = {
        'site': site,
        'comment': comment,
        'content_object': content_object
    }

    message = render_to_string("comments/comment_notification_email.txt", context, request=request)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)


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
        super(CommentsRelation, self).__init__(
            to=get_comments_model(),
            content_type_field='content_type',
            object_id_field='object_pk',
            **kwargs
        )
