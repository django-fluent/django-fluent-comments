from django.template import Library
from django.core import context_processors

register = Library()

@register.inclusion_tag("fluent_comments/templatetags/ajax_comment_tags.html", takes_context=True)
def ajax_comment_tags(context):
    request = context['request']

    new_context = {}
    new_context.update(context_processors.static(request))
    return new_context
