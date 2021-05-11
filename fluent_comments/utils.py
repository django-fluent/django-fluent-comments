"""
Internal utils
"""
import re

from django.contrib.contenttypes.models import ContentType

from fluent_comments import appsettings


RE_INTERPUNCTION = re.compile(r"\W+")


def get_comment_template_name(comment):
    """
    Internal function for the rendering of comments.
    """
    ctype = ContentType.objects.get_for_id(comment.content_type_id)
    return [
        "comments/%s/%s/comment.html" % (ctype.app_label, ctype.model),
        "comments/%s/comment.html" % ctype.app_label,
        "comments/comment.html",
    ]


def get_comment_context_data(comment, action=None):
    """
    Internal function for the rendering of comments.
    """
    return {
        "comment": comment,
        "action": action,
        "preview": (action == "preview"),
        "USE_THREADEDCOMMENTS": appsettings.USE_THREADEDCOMMENTS,
    }


def split_words(comment):
    """
    Internal function to split words
    """
    return set(RE_INTERPUNCTION.sub(" ", comment).split())
