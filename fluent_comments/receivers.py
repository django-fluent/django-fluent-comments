import re

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_comments import signals

from fluent_comments import appsettings

try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.9+
except ImportError:
    from django.contrib.sites.models import get_current_site


WHITESPACE = re.compile(r'\s+')


@receiver(signals.comment_was_posted)
def on_comment_posted(sender, comment, request, **kwargs):
    """
    Send email notification of a new comment to site staff when email notifications have been requested.
    """
    # This code is copied from django_comments.moderation.
    # That code doesn't offer a RequestContext, which makes it really
    # hard to generate proper URL's with FQDN in the email
    #
    # Instead of implementing this feature in the moderator class, the signal is used instead
    # so the notification feature works regardless of a manual moderator.register() call in the project.
    if not appsettings.FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION:
        return

    recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
    site = get_current_site(request)
    content_object = comment.content_object

    if comment.is_removed:
        subject = u'[{0}] Spam comment on "{1}"'.format(site.name, content_object)
    elif not comment.is_public:
        subject = u'[{0}] Moderated comment on "{1}"'.format(site.name, content_object)
    else:
        subject = u'[{0}] New comment posted on "{1}"'.format(site.name, content_object)

    context = {
        'site': site,
        'comment': comment,
        'content_object': content_object
    }

    message = render_to_string("comments/comment_notification_email.txt", context, request=request)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
