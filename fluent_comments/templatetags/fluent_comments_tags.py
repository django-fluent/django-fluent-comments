from django.template import Library
from django.core import context_processors
from fluent_comments.moderation import comments_are_closed, comments_are_moderated

register = Library()

@register.inclusion_tag("fluent_comments/templatetags/ajax_comment_tags.html", takes_context=True)
def ajax_comment_tags(context):
    """
    Display the required ``<div>`` elements to let the Ajax comment functionality work with your form.
    """
    request = context['request']

    new_context = {}
    new_context.update(context_processors.static(request))
    return new_context


register.filter('comments_are_closed', comments_are_closed)
register.filter('comments_are_moderated', comments_are_moderated)
