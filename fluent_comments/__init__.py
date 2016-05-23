"""
API for :ref:`custom-comment-app-api`
"""
from fluent_comments import appsettings

# following PEP 440
__version__ = "1.2.1"


def get_model():
    """
    Return the model to use for commenting.
    """
    if appsettings.USE_THREADEDCOMMENTS:
        from threadedcomments.models import ThreadedComment
        return ThreadedComment
    else:
        # Our proxy model that performs select_related('user') for the comments
        from fluent_comments.models import FluentComment
        return FluentComment


def get_form():
    """
    Return the form to use for commenting.
    """
    from fluent_comments.forms import FluentCommentForm
    return FluentCommentForm
