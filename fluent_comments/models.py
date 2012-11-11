from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.comments import signals
from django.shortcuts import render
from fluent_comments import appsettings


@receiver(signals.comment_was_posted)
def on_comment_posted(sender, comment, request, **kwargs):
    """
    Send email notification of a new comment to site staff when email notifications have been requested.
    """
    # This code is copied from django.contrib.comments.moderation.
    # That code doesn't offer a RequestContext, which makes it really
    # hard to generate proper URL's with FQDN in the email
    #
    # Instead of implementing this feature in the moderator class, the signal is used instead
    # so the notification feature works regardless of a manual moderator.register() call in the project.
    if not appsettings.FLUENT_COMMENTS_USE_EMAIL_MODERATION:
        return

    recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
    site = get_current_site(request)
    content_object = comment.content_object

    subject = '[{0}] New comment posted on "{1}"'.format(site.name, content_object)
    context = {
        'site': site,
        'comment': comment,
        'content_object': content_object
    }

    message = render(request, "comments/comment_notification_email.txt", context)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
