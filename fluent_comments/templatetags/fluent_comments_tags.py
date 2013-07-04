from django.conf import settings
from django.template import Library, Node
from django.core import context_processors
from django.template.loader import get_template
from fluent_comments import appsettings
from fluent_comments.models import get_comments_for_model
from fluent_comments.moderation import comments_are_open, comments_are_moderated

register = Library()

@register.inclusion_tag("fluent_comments/templatetags/ajax_comment_tags.html", takes_context=True)
def ajax_comment_tags(context, for_, target_object):
    """
    Display the required ``<div>`` elements to let the Ajax comment functionality work with your form.
    """
    new_context = {
        'STATIC_URL': context.get('STATIC_URL', None),
        'USE_THREADEDCOMMENTS': appsettings.USE_THREADEDCOMMENTS,
        'target_object': target_object,
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


class FluentCommentsList(Node):
    def render(self, context):
        # Include proper template, avoid parsing it twice by operating like @register.inclusion_tag()
        if not getattr(self, 'nodelist', None):
            if appsettings.USE_THREADEDCOMMENTS:
                template = get_template("fluent_comments/templatetags/threaded_list.html")
            else:
                template = get_template("fluent_comments/templatetags/flat_list.html")
            self.nodelist = template

        # NOTE NOTE NOTE
        # HACK: Determine the parent object based on the comment list queryset.
        # the {% render_comment_list for article %} tag does not pass the object in a general form to the template.
        # Not assuming that 'object.pk' holds the correct value.
        #
        # This obviously doesn't work when the list is empty.
        # To address that, the client-side code also fixes that, by looking for the object ID in the nearby form.
        target_object_id = context.get('target_object_id', None)
        if not target_object_id:
            comment_list = context['comment_list']
            if isinstance(comment_list, list) and comment_list:
                target_object_id = comment_list[0].object_pk

        # Render the node
        context['USE_THREADEDCOMMENTS'] = appsettings.USE_THREADEDCOMMENTS
        context['target_object_id'] = target_object_id
        return self.nodelist.render(context)


@register.tag
def fluent_comments_list(parser, token):
    """
    A tag to select the proper template for the current comments app.
    """
    return FluentCommentsList()
