from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_text

try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.9+
except ImportError:
    from django.contrib.sites.models import get_current_site


def send_comment_posted(comment, request):
    """
    Send the email to staff that an comment was posted.

    While the django_comments module has email support,
    it doesn't pass the 'request' to the context.
    This also changes the subject to show the page title.
    """
    recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
    site = get_current_site(request)
    content_object = comment.content_object
    content_title = force_text(content_object)

    if comment.is_removed:
        subject = u'[{0}] Spam comment on "{1}"'.format(site.name, content_title)
    elif not comment.is_public:
        subject = u'[{0}] Moderated comment on "{1}"'.format(site.name, content_title)
    else:
        subject = u'[{0}] New comment posted on "{1}"'.format(site.name, content_title)

    context = {
        'site': site,
        'comment': comment,
        'content_object': content_object
    }

    message = render_to_string("comments/comment_notification_email.txt", context, request=request)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
