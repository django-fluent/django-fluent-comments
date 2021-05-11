from urllib.parse import urljoin

from akismet import Akismet, SpamStatus
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import smart_str

import fluent_comments
from fluent_comments import appsettings


def akismet_check(comment, content_object, request):
    """
    Connects to Akismet and evaluates to True if Akismet marks this comment as spam.

    :rtype: akismet.SpamStatus
    """
    # Return previously cached response
    akismet_result = getattr(comment, "_akismet_result_", None)
    if akismet_result is not None:
        return akismet_result

    # Get Akismet data
    AKISMET_API_KEY = appsettings.AKISMET_API_KEY
    if not AKISMET_API_KEY:
        raise ImproperlyConfigured(
            "You must set AKISMET_API_KEY to use comment moderation with Akismet."
        )

    current_domain = get_current_site(request).domain
    auto_blog_url = "{0}://{1}/".format(request.is_secure() and "https" or "http", current_domain)
    blog_url = appsettings.AKISMET_BLOG_URL or auto_blog_url

    akismet = Akismet(
        AKISMET_API_KEY,
        blog=blog_url,
        is_test=int(bool(appsettings.AKISMET_IS_TEST)),
        application_user_agent="django-fluent-comments/{0}".format(fluent_comments.__version__),
    )

    akismet_data = _get_akismet_data(blog_url, comment, content_object, request)
    akismet_result = akismet.check(**akismet_data)  # raises AkismetServerError when key is invalid
    setattr(comment, "_akismet_result_", akismet_result)
    return akismet_result


def _get_akismet_data(blog_url, comment, content_object, request):
    # Field documentation:
    # http://akismet.com/development/api/#comment-check
    data = {
        # Comment info
        "permalink": urljoin(blog_url, content_object.get_absolute_url()),
        # see http://blog.akismet.com/2012/06/19/pro-tip-tell-us-your-comment_type/
        "comment_type": "comment",  # comment, trackback, pingback
        "comment_author": getattr(comment, "name", ""),
        "comment_author_email": getattr(comment, "email", ""),
        "comment_author_url": getattr(comment, "url", ""),
        "comment_content": smart_str(comment.comment),
        "comment_date": comment.submit_date,
        # Request info
        "referrer": request.META.get("HTTP_REFERER", ""),
        "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        "user_ip": comment.ip_address,
    }

    if comment.user_id and comment.user.is_superuser:
        data["user_role"] = "administrator"  # always passes test

    # If the language is known, provide it.
    language = _get_article_language(content_object)
    if language:
        data["blog_lang"] = language

    return data


def _get_article_language(article):
    try:
        # django-parler uses this attribute
        return article.get_current_language()
    except AttributeError:
        pass

    try:
        return article.language_code
    except AttributeError:
        pass

    return None
