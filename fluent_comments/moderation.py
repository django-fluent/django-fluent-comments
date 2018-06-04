from __future__ import absolute_import

import logging

from akismet import SpamStatus
from django_comments.moderation import moderator, CommentModerator

from fluent_comments import appsettings
from fluent_comments.akismet import akismet_check
from fluent_comments.email import send_comment_posted
from fluent_comments.utils import split_words

try:
    from urllib.parse import urljoin  # Python 3
except ImportError:
    from urlparse import urljoin  # Python 2

logger = logging.getLogger(__name__)

# Akismet code originally based on django-comments-spamfighter.

__all__ = (
    'FluentCommentsModerator',
    'moderate_model',
    'get_model_moderator',
    'comments_are_open',
    'comments_are_moderated',
)


class FluentCommentsModerator(CommentModerator):
    """
    Moderation policy for fluent-comments.
    """
    auto_close_field = None
    auto_moderate_field = None
    enable_field = None

    close_after = appsettings.FLUENT_COMMENTS_CLOSE_AFTER_DAYS
    moderate_after = appsettings.FLUENT_COMMENTS_MODERATE_AFTER_DAYS
    email_notification = False   # Using signals instead
    akismet_check = appsettings.FLUENT_CONTENTS_USE_AKISMET
    akismet_check_action = appsettings.FLUENT_COMMENTS_AKISMET_ACTION
    moderate_bad_words = set(appsettings.FLUENT_COMMENTS_MODERATE_BAD_WORDS)

    def allow(self, comment, content_object, request):
        """
        Determine whether a given comment is allowed to be posted on a given object.

        Returns ``True`` if the comment should be allowed, ``False`` otherwise.
        """
        # Parent class check
        if not super(FluentCommentsModerator, self).allow(comment, content_object, request):
            return False

        # Akismet check
        if self.akismet_check:
            akismet_result = akismet_check(comment, content_object, request)
            if self.akismet_check_action == 'delete' and akismet_result in (SpamStatus.ProbableSpam, SpamStatus.DefiniteSpam):
                return False  # Akismet marked the comment as spam.
            elif self.akismet_check_action == 'auto' and akismet_result == SpamStatus.DefiniteSpam:
                return False  # Clearly spam

        return True

    def moderate(self, comment, content_object, request):
        """
        Determine whether a given comment on a given object should be allowed to show up immediately,
        or should be marked non-public and await approval.

        Returns ``True`` if the comment should be moderated (marked non-public), ``False`` otherwise.
        """

        # Soft delete checks are done first, so these comments are not mistakenly "just moderated"
        # for expiring the `close_after` date, but correctly get marked as spam instead.
        # This helps staff to quickly see which comments need real moderation.
        if self.akismet_check:
            akismet_result = akismet_check(comment, content_object, request)
            if akismet_result:
                # Typically action=delete never gets here, unless the service was having problems.
                if akismet_result in (SpamStatus.ProbableSpam, SpamStatus.DefiniteSpam) and \
                       self.akismet_check_action in ('auto', 'soft_delete', 'delete'):
                   comment.is_removed = True  # Set extra marker

                # SpamStatus.Unknown or action=moderate will end up in the moderation queue
                return True

        # Parent class check
        if super(FluentCommentsModerator, self).moderate(comment, content_object, request):
            return True

        # Bad words check
        if self.moderate_bad_words:
            input_words = split_words(comment.comment)
            if self.moderate_bad_words.intersection(input_words):
                return True

        # Akismet check
        if self.akismet_check and self.akismet_check_action not in ('soft_delete', 'delete'):
            # Return True if akismet marks this comment as spam and we want to moderate it.
            if akismet_check(comment, content_object, request):
                return True

        return False


def moderate_model(ParentModel, publication_date_field=None, enable_comments_field=None):
    """
    Register a parent model (e.g. ``Blog`` or ``Article``) that should receive comment moderation.

    :param ParentModel: The parent model, e.g. a ``Blog`` or ``Article`` model.
    :param publication_date_field: The field name of a :class:`~django.db.models.DateTimeField` in the parent model which stores the publication date.
    :type publication_date_field: str
    :param enable_comments_field: The field name of a :class:`~django.db.models.BooleanField` in the parent model which stores the whether comments are enabled.
    :type enable_comments_field: str
    """
    attrs = {
        'auto_close_field': publication_date_field,
        'auto_moderate_field': publication_date_field,
        'enable_field': enable_comments_field,
    }
    ModerationClass = type(ParentModel.__name__ + 'Moderator', (FluentCommentsModerator,), attrs)
    moderator.register(ParentModel, ModerationClass)


def get_model_moderator(model):
    """
    Return the moderator class that is registered with a content object.
    If there is no associated moderator with a class, None is returned.

    :param model: The Django model registered with :func:`moderate_model`
    :type model: :class:`~django.db.models.Model`
    :return: The moderator class which holds the moderation policies.
    :rtype: :class:`~django_comments.moderation.CommentModerator`
    """
    try:
        return moderator._registry[model]
    except KeyError:
        return None


def comments_are_open(content_object):
    """
    Return whether comments are still open for a given target object.
    """
    moderator = get_model_moderator(content_object.__class__)
    if moderator is None:
        return True

    # Check the 'enable_field', 'auto_close_field' and 'close_after',
    # by reusing the basic Django policies.
    return CommentModerator.allow(moderator, None, content_object, None)


def comments_are_moderated(content_object):
    """
    Return whether comments are moderated for a given target object.
    """
    moderator = get_model_moderator(content_object.__class__)
    if moderator is None:
        return False

    # Check the 'auto_moderate_field', 'moderate_after',
    # by reusing the basic Django policies.
    return CommentModerator.moderate(moderator, None, content_object, None)
