"""
API for :ref:`custom-comment-app-api`
"""
from django.contrib.comments import Comment
from fluent_comments import appsettings
from fluent_comments.forms import FluentCommentForm


# following PEP 386
__version__ = "1.0a1"


if appsettings.USE_THREADEDCOMMENTS:
    # Extend the API provided by django-threadedcomments,
    # in case this app uses more hooks of Django's custom comment app API.
    from threadedcomments import *


def get_model():
    """
    Return the model to use for commenting.
    """
    if appsettings.USE_THREADEDCOMMENTS:
        return ThreadedComment
    else:
        return Comment


def get_form():
    """
    Return the form to use for commenting.
    """
    return FluentCommentForm
