"""
API for :ref:`custom-comment-app-api`
"""
from fluent_comments import appsettings
from fluent_comments.models import FluentComment
from fluent_comments.forms import FluentCommentForm


# following PEP 440
__version__ = "1.0.4"


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
        # Our proxy model that performs select_related('user') for the comments
        return FluentComment


def get_form():
    """
    Return the form to use for commenting.
    """
    return FluentCommentForm
