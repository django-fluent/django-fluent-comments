"""
API for :ref:`custom-comment-app-api`
"""
from django.contrib.comments import Comment
from fluent_comments import appsettings
from fluent_comments.forms import FluentCommentForm


def get_model():
    """
    Return the model to use for commenting.
    """
    if appsettings.USE_THREADEDCOMMENTS:
        from threadedcomments.models import ThreadedComment
        return ThreadedComment
    else:
        return Comment


def get_form():
    """
    Return the form to use for commenting.
    """
    return FluentCommentForm
