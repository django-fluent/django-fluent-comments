from django.conf import settings
from django.template import Library
from django.core import context_processors
from django.template.loader import get_template
from fluent_comments import appsettings
from fluent_comments.models import get_comments_for_model
from fluent_comments.moderation import comments_are_open, comments_are_moderated

register = Library()

@register.inclusion_tag("fluent_comments/templatetags/ajax_comment_tags.html", takes_context=True)
def ajax_comment_tags(context):
    """
    Display the required ``<div>`` elements to let the Ajax comment functionality work with your form.
    """
    new_context = {
        'STATIC_URL': context.get('STATIC_URL', None),
        'USE_THREADEDCOMMENTS': appsettings.USE_THREADEDCOMMENTS,
    }

    # Be configuration independent:
    if new_context['STATIC_URL'] is None:
        try:
            request = context['request']
        except KeyError:
            new_context.update({'STATIC_URL': settings.STATIC_URL})
        else:
            new_context.update(context_processors.static(request))

    return new_context


register.filter('comments_are_open', comments_are_open)
register.filter('comments_are_moderated', comments_are_moderated)


@register.filter
def comments_count(content_object):
    """
    Return the number of comments posted at a target object.

    You can use this instead of the ``{% get_comment_count for [object] as [varname]  %}`` tag.
    """
    return get_comments_for_model(content_object).count()


@register.simple_tag(takes_context=True)
def fluent_comments_list(context):
    """
    A simple tag to select the proper template for the current comments app.
    """
    if appsettings.USE_THREADEDCOMMENTS:
        template = get_template("fluent_comments/templatetags/threaded_list.html")
    else:
        template = get_template("fluent_comments/templatetags/flat_list.html")

    context['USE_THREADEDCOMMENTS'] = appsettings.USE_THREADEDCOMMENTS
    return template.render(context)
