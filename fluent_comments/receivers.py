"""
The comment signals are handled to fallback to a default moderator.

This avoids not checking for spam or sending email notifications
for comments that bypassed the moderator registration
(e.g. posting a comment on a different page).

This is especially useful when a django-fluent-contents "CommentsAreaItem"
element is added to a random page subclass (which is likely not registered).
"""
import logging

import django_comments
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import receiver
from django.utils.module_loading import import_string
from django_comments import signals

from fluent_comments import appsettings, moderation

logger = logging.getLogger(__name__)


def load_default_moderator():
    """
    Find a moderator object
    """
    if appsettings.FLUENT_COMMENTS_DEFAULT_MODERATOR == "default":
        # Perform spam checks
        return moderation.FluentCommentsModerator(None)
    elif appsettings.FLUENT_COMMENTS_DEFAULT_MODERATOR == "deny":
        # Deny all comments not from known registered models.
        return moderation.AlwaysDeny(None)
    elif str(appsettings.FLUENT_COMMENTS_DEFAULT_MODERATOR).lower() == "none":
        # Disables default moderator
        return moderation.NullModerator(None)
    elif "." in appsettings.FLUENT_COMMENTS_DEFAULT_MODERATOR:
        return import_string(appsettings.FLUENT_COMMENTS_DEFAULT_MODERATOR)(None)
    else:
        raise ImproperlyConfigured(
            "Bad FLUENT_COMMENTS_DEFAULT_MODERATOR value. Provide default/deny/none or a dotted path"
        )


default_moderator = load_default_moderator()
CommentModel = django_comments.get_model()


@receiver(signals.comment_will_be_posted)
def on_comment_will_be_posted(sender, comment, request, **kwargs):
    """
    Make sure both the Ajax and regular comments are checked for moderation.
    This signal is also used to link moderators to the comment posting.
    """
    content_object = comment.content_object
    moderator = moderation.get_model_moderator(content_object.__class__)
    if moderator and comment.__class__ is not CommentModel:
        # Help with some hard to diagnose problems. The default Django moderator connects
        # to the configured comment model. When this model differs from the signal sender,
        # the the form stores a different model then COMMENTS_APP provides.
        moderator = None
        logger.warning(
            "Comment of type '%s' was not moderated by '%s', "
            "because the parent '%s' has a moderator installed for '%s' instead",
            comment.__class__.__name__,
            moderator.__class__.__name__,
            content_object.__class__.__name__,
            CommentModel.__name__,
        )

    if moderator is None:
        logger.info(
            "Using default moderator for comment '%s' on parent '%s'",
            comment.__class__.__name__,
            content_object.__class__.__name__,
        )
        _run_default_moderator(comment, content_object, request)


def _run_default_moderator(comment, content_object, request):
    """
    Run the default moderator
    """
    # The default moderator will likely not check things like "auto close".
    # It can still provide akismet and bad word checking.
    if not default_moderator.allow(comment, content_object, request):
        # Comment will be disallowed outright (HTTP 403 response)
        return False

    if default_moderator.moderate(comment, content_object, request):
        comment.is_public = False


@receiver(signals.comment_was_posted)
def on_comment_posted(sender, comment, request, **kwargs):
    """
    Send email notification of a new comment to site staff when email notifications have been requested.
    """
    content_object = comment.content_object

    moderator = moderation.get_model_moderator(content_object.__class__)
    if moderator is None or comment.__class__ is not CommentModel:
        # No custom moderator means no email would be sent.
        # This still pass the comment to the default moderator.
        default_moderator.email(comment, content_object, request)
